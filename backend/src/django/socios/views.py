from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.paginator import EmptyPage, Paginator
from django.db import DatabaseError, IntegrityError
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Cobro, Socio
from .serializers import (
    CobroLoteSerializer,
    CobroSerializer,
    CobrosResumenQuerySerializer,
    SocioSerializer,
)


def validation_error_payload(serializer):
    return {
        "mensaje": "Datos invalidos",
        "errores": serializer.errors,
    }


class SocioList(generics.ListCreateAPIView):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            data = self.get_serializer(queryset, many=True).data
            return Response(data)
        except DatabaseError:
            return Response([])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            self.perform_create(serializer)
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SocioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer

    def _get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            return None

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        socio = self._get_object_or_none()
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(socio).data)

    def update(self, request, *args, **kwargs):
        socio = self._get_object_or_none()
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(socio, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            self.perform_update(serializer)
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        socio = self._get_object_or_none()
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(socio)
        return Response({"mensaje": "Socio eliminado"})


class CobroList(generics.ListCreateAPIView):
    queryset = Cobro.objects.select_related("socio").all().order_by("-anio", "-mes", "id")
    serializer_class = CobroSerializer

    def _normalizar_datos(self, payload):
        data = payload.copy()
        monto_pagado = data.get("monto_pagado")
        fecha_registro_pago = data.get("fecha_registro_pago")
        tipo_cobro = data.get("tipo_cobro", Cobro.TIPO_MENSUAL)

        if monto_pagado is not None and str(monto_pagado) != "" and not fecha_registro_pago:
            try:
                if Decimal(str(monto_pagado)) > 0:
                    data["fecha_registro_pago"] = date.today().isoformat()
            except Exception:
                pass

        if tipo_cobro == Cobro.TIPO_DIA_CANCHA and "monto_cuota" not in data and monto_pagado is not None:
            data["monto_cuota"] = monto_pagado

        return data

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            paginator = Paginator(queryset, 10)
            page_number = request.query_params.get("page", 1)

            try:
                page_obj = paginator.page(page_number)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages if paginator.num_pages else 1)

            serializer = self.get_serializer(page_obj.object_list, many=True)
            return Response(
                {
                    "items": serializer.data,
                    "total_pages": paginator.num_pages if paginator.num_pages else 1,
                    "total_count": paginator.count,
                    "page_size": paginator.per_page,
                }
            )
        except DatabaseError:
            return Response({"items": [], "total_pages": 1, "total_count": 0, "page_size": 10})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self._normalizar_datos(request.data))
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        tipo_cobro = serializer.validated_data.get("tipo_cobro", Cobro.TIPO_MENSUAL)
        if tipo_cobro == Cobro.TIPO_DIA_CANCHA:
            socio = serializer.validated_data["socio"]
            anio = serializer.validated_data["anio"]
            mes = serializer.validated_data["mes"]
            monto_nuevo = serializer.validated_data.get("monto_pagado", Decimal("0"))

            existente = Cobro.objects.filter(
                socio=socio,
                anio=anio,
                mes=mes,
                tipo_cobro=Cobro.TIPO_DIA_CANCHA,
            ).first()
            if existente:
                existente.monto_pagado = existente.monto_pagado + monto_nuevo
                existente.monto_cuota = existente.monto_pagado
                existente.fecha_registro_pago = serializer.validated_data.get("fecha_registro_pago")
                existente.metodo_pago = serializer.validated_data.get("metodo_pago", "")
                existente.observaciones = serializer.validated_data.get("observaciones", "")
                existente.save()
                out = self.get_serializer(existente)
                return Response(out.data, status=status.HTTP_200_OK)

        try:
            self.perform_create(serializer)
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CobroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cobro.objects.select_related("socio").all()
    serializer_class = CobroSerializer

    def _get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            return None

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        cobro = self._get_object_or_none()
        if cobro is None:
            return Response({"mensaje": "Cobro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(cobro).data)

    def update(self, request, *args, **kwargs):
        cobro = self._get_object_or_none()
        if cobro is None:
            return Response({"mensaje": "Cobro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop("partial", False)
        data = request.data.copy()
        monto_pagado = data.get("monto_pagado")
        tipo_cobro = data.get("tipo_cobro", cobro.tipo_cobro)
        if monto_pagado is not None and str(monto_pagado) != "":
            try:
                if Decimal(str(monto_pagado)) > 0 and not data.get("fecha_registro_pago"):
                    data["fecha_registro_pago"] = date.today().isoformat()
            except Exception:
                pass

        if tipo_cobro == Cobro.TIPO_DIA_CANCHA:
            monto_actual = cobro.monto_pagado
            monto_nuevo = Decimal(str(monto_pagado)) if monto_pagado is not None and str(monto_pagado) != "" else Decimal("0")
            data["monto_pagado"] = monto_actual + monto_nuevo
            data["monto_cuota"] = monto_actual + monto_nuevo

        serializer = self.get_serializer(cobro, data=data, partial=partial)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            self.perform_update(serializer)
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cobro = self._get_object_or_none()
        if cobro is None:
            return Response({"mensaje": "Cobro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(cobro)
        return Response({"mensaje": "Cobro eliminado"})


class CobroResumenAnual(generics.GenericAPIView):
    serializer_class = CobroSerializer

    def get(self, request, *args, **kwargs):
        query_serializer = CobrosResumenQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        anio = query_serializer.validated_data.get("anio", date.today().year)

        socios = Socio.objects.all().order_by("apellido", "nombre")
        cobros = Cobro.objects.filter(anio=anio).select_related("socio")
        cobros_map = {}
        for c in cobros:
            key = (c.socio_id, c.mes)
            if key not in cobros_map:
                cobros_map[key] = {"monto_cuota": Decimal("0"), "monto_pagado": Decimal("0"), "fecha": None}
            cobros_map[key]["monto_cuota"] += c.monto_cuota
            cobros_map[key]["monto_pagado"] += c.monto_pagado
            if c.fecha_registro_pago and (
                cobros_map[key]["fecha"] is None or c.fecha_registro_pago > cobros_map[key]["fecha"]
            ):
                cobros_map[key]["fecha"] = c.fecha_registro_pago

        socios_resumen = []
        deuda_global = Decimal("0")
        socios_con_deuda = 0

        for socio in socios:
            resumen_mensual = []
            deuda_total = Decimal("0")

            for mes in range(1, 13):
                cobro = cobros_map.get((socio.id, mes))
                if cobro:
                    monto_cuota = cobro["monto_cuota"]
                    monto_pagado = cobro["monto_pagado"]
                    saldo = monto_cuota - monto_pagado
                    saldo = saldo if saldo > 0 else Decimal("0")

                    if monto_pagado <= 0:
                        estado = "Pendiente"
                    elif monto_pagado < monto_cuota:
                        estado = "Parcial"
                    else:
                        estado = "Pagado"

                    fecha_registro_pago = cobro["fecha"]
                else:
                    monto_cuota = Decimal("0")
                    monto_pagado = Decimal("0")
                    saldo = Decimal("0")
                    estado = "Sin registro"
                    fecha_registro_pago = None

                deuda_total += saldo
                resumen_mensual.append(
                    {
                        "mes": mes,
                        "monto_cuota": float(monto_cuota),
                        "monto_pagado": float(monto_pagado),
                        "saldo_mes": float(saldo),
                        "estado": estado,
                        "fecha_registro_pago": fecha_registro_pago,
                    }
                )

            if deuda_total > 0:
                socios_con_deuda += 1

            deuda_global += deuda_total
            socios_resumen.append(
                {
                    "socio_id": socio.id,
                    "socio_nombre": f"{socio.nombre} {socio.apellido}".strip(),
                    "registra_deuda": socio.registra_deuda,
                    "deuda_total": float(deuda_total),
                    "resumen_mensual": resumen_mensual,
                }
            )

        return Response(
            {
                "anio": anio,
                "meses": list(range(1, 13)),
                "socios": socios_resumen,
                "totales": {
                    "deuda_global": float(deuda_global),
                    "cantidad_socios_con_deuda": socios_con_deuda,
                },
            }
        )


class CobroLoteCreate(generics.GenericAPIView):
    serializer_class = CobroLoteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        socios_ids = list(dict.fromkeys(data["socios_ids"]))
        anio = data["anio"]
        mes = data["mes"]
        tipo_cobro = data.get("tipo_cobro", Cobro.TIPO_MENSUAL)
        monto_cuota = data["monto_cuota"]
        monto_pagado = data.get("monto_pagado", Decimal("0"))
        fecha_registro_pago = data.get("fecha_registro_pago")
        metodo_pago = data.get("metodo_pago", "")
        observaciones = data.get("observaciones", "")
        actualizar_existentes = data.get("actualizar_existentes", False)
        usar_todos_los_socios = data.get("usar_todos_los_socios", False)
        marcar_todos_como_usuarios_socio = data.get("marcar_todos_como_usuarios_socio", False)

        if usar_todos_los_socios:
            socios_ids = list(Socio.objects.values_list("id", flat=True))

        if monto_pagado > 0 and not fecha_registro_pago:
            fecha_registro_pago = date.today()

        socios = Socio.objects.in_bulk(socios_ids)

        creados = []
        actualizados = []
        omitidos = []
        errores = []

        usuarios_socio_resultado = {
            "marcados": 0,
            "ya_eransocio": 0,
            "sin_usuario": 0,
            "detalle_sin_usuario": [],
        }

        if marcar_todos_como_usuarios_socio:
            grupo_socio, _ = Group.objects.get_or_create(name="socio")
            todos_los_socios = Socio.objects.all()

            for socio in todos_los_socios:
                user = None
                if socio.dni:
                    user = User.objects.filter(username=socio.dni).first()

                if not user and socio.email:
                    user = User.objects.filter(email=socio.email).first()

                if not user:
                    usuarios_socio_resultado["sin_usuario"] += 1
                    usuarios_socio_resultado["detalle_sin_usuario"].append(
                        {
                            "socio_id": socio.id,
                            "socio_nombre": f"{socio.nombre} {socio.apellido}".strip(),
                        }
                    )
                    continue

                if user.groups.filter(name="socio").exists():
                    usuarios_socio_resultado["ya_eransocio"] += 1
                    continue

                user.groups.add(grupo_socio)
                usuarios_socio_resultado["marcados"] += 1

        for socio_id in socios_ids:
            socio = socios.get(socio_id)
            if not socio:
                errores.append({"socio_id": socio_id, "mensaje": "Socio no encontrado"})
                continue

            try:
                cobro, fue_creado = Cobro.objects.get_or_create(
                    socio=socio,
                    anio=anio,
                    mes=mes,
                    tipo_cobro=tipo_cobro,
                    defaults={
                        "monto_cuota": monto_cuota,
                        "monto_pagado": monto_pagado,
                        "fecha_registro_pago": fecha_registro_pago,
                        "metodo_pago": metodo_pago,
                        "observaciones": observaciones,
                    },
                )

                if fue_creado:
                    creados.append(
                        {
                            "socio_id": socio_id,
                            "socio_nombre": f"{socio.nombre} {socio.apellido}".strip(),
                            "cobro_id": cobro.id,
                        }
                    )
                    continue

                if tipo_cobro == Cobro.TIPO_DIA_CANCHA:
                    cobro.monto_pagado = cobro.monto_pagado + monto_pagado
                    cobro.monto_cuota = cobro.monto_pagado
                    cobro.fecha_registro_pago = fecha_registro_pago
                    cobro.metodo_pago = metodo_pago
                    cobro.observaciones = observaciones
                    cobro.tipo_cobro = tipo_cobro
                    cobro.save()

                    actualizados.append(
                        {
                            "socio_id": socio_id,
                            "socio_nombre": f"{socio.nombre} {socio.apellido}".strip(),
                            "cobro_id": cobro.id,
                        }
                    )
                    continue

                if not actualizar_existentes:
                    omitidos.append(
                        {
                            "socio_id": socio_id,
                            "socio_nombre": f"{socio.nombre} {socio.apellido}".strip(),
                            "mensaje": "Ya existe cobro para ese período",
                        }
                    )
                    continue

                cobro.monto_cuota = monto_cuota
                if tipo_cobro == Cobro.TIPO_DIA_CANCHA:
                    cobro.monto_pagado = cobro.monto_pagado + monto_pagado
                    cobro.monto_cuota = cobro.monto_pagado
                else:
                    cobro.monto_pagado = monto_pagado
                cobro.fecha_registro_pago = fecha_registro_pago
                cobro.metodo_pago = metodo_pago
                cobro.observaciones = observaciones
                cobro.tipo_cobro = tipo_cobro
                cobro.save()

                actualizados.append(
                    {
                        "socio_id": socio_id,
                        "socio_nombre": f"{socio.nombre} {socio.apellido}".strip(),
                        "cobro_id": cobro.id,
                    }
                )
            except Exception as exc:
                errores.append({"socio_id": socio_id, "mensaje": str(exc)})

        return Response(
            {
                "mensaje": "Lote de cobros procesado",
                "periodo": {"anio": anio, "mes": mes},
                "resumen": {
                    "creados": len(creados),
                    "actualizados": len(actualizados),
                    "omitidos": len(omitidos),
                    "errores": len(errores),
                    "usuarios_socio": usuarios_socio_resultado,
                },
                "detalle": {
                    "creados": creados,
                    "actualizados": actualizados,
                    "omitidos": omitidos,
                    "errores": errores,
                },
            }
        )
