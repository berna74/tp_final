from rest_framework import serializers

from .models import Cobro, MovimientoFinanciero, Pago, Socio
from .roles import ROLE_ADMIN, ROLE_SUPERADMIN, resolver_rol_usuario


class SocioSerializer(serializers.ModelSerializer):
    categorias = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )

    class Meta:
        model = Socio
        fields = [
            "id",
            "nombre",
            "apellido",
            "dni",
            "email",
            "telefono",
            "fecha_inscripcion",
            "profesor_id",
            "registra_deuda",
            "categorias",
        ]
        extra_kwargs = {
            "nombre": {"required": False, "allow_blank": True},
            "apellido": {"required": False, "allow_blank": True},
            "dni": {"required": False, "allow_blank": True},
            "email": {"required": False, "allow_blank": True},
            "telefono": {"required": False, "allow_blank": True},
            "fecha_inscripcion": {"required": False, "allow_null": True},
            "profesor_id": {"required": False, "allow_null": True},
            "registra_deuda": {"required": False},
        }

    def create(self, validated_data):
        validated_data.pop("categorias", None)
        validated_data.setdefault("nombre", "")
        validated_data.setdefault("apellido", "")
        validated_data.setdefault("dni", "")
        validated_data.setdefault("email", "")
        validated_data.setdefault("telefono", "")
        validated_data.setdefault("registra_deuda", False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("categorias", None)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["categorias"] = []
        request = self.context.get("request")
        user = getattr(request, "user", None) if request is not None else None
        if not user or not user.is_authenticated:
            data["dni"] = ""
            return data

        rol = resolver_rol_usuario(user)
        if rol not in {ROLE_SUPERADMIN, ROLE_ADMIN}:
            data["dni"] = ""
        return data


class SociosListQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, min_value=1, default=1)


class SociosPaginatedResponseSerializer(serializers.Serializer):
    items = SocioSerializer(many=True)
    total_pages = serializers.IntegerField(min_value=1)
    total_count = serializers.IntegerField(min_value=0)
    page_size = serializers.IntegerField(min_value=1)


class CobroSerializer(serializers.ModelSerializer):
    socio_nombre = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    saldo_mes = serializers.SerializerMethodField()

    class Meta:
        model = Cobro
        fields = [
            "id",
            "socio",
            "socio_nombre",
            "anio",
            "mes",
            "tipo_cobro",
            "monto_cuota",
            "monto_pagado",
            "marcar_en_rojo",
            "saldo_mes",
            "estado",
            "fecha_registro_pago",
            "metodo_pago",
            "observaciones",
        ]
        extra_kwargs = {
            "fecha_registro_pago": {"required": False, "allow_null": True},
            "metodo_pago": {"required": False, "allow_blank": True},
            "observaciones": {"required": False, "allow_blank": True},
        }

    def get_socio_nombre(self, obj):
        return f"{obj.socio.nombre} {obj.socio.apellido}".strip()

    def get_saldo_mes(self, obj):
        saldo = obj.monto_cuota - obj.monto_pagado
        return float(saldo) if saldo > 0 else 0.0

    def get_estado(self, obj):
        if obj.monto_pagado <= 0:
            return "Pendiente"
        if obj.monto_pagado < obj.monto_cuota:
            return "Parcial"
        return "Pagado"


class CobrosPaginatedResponseSerializer(serializers.Serializer):
    items = CobroSerializer(many=True)
    total_pages = serializers.IntegerField(min_value=1)
    total_count = serializers.IntegerField(min_value=0)
    page_size = serializers.IntegerField(min_value=1)


class CobrosResumenQuerySerializer(serializers.Serializer):
    anio = serializers.IntegerField(required=False, min_value=2000)


class CobroLoteSerializer(serializers.Serializer):
    socios_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )
    socios_rojo_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        required=False,
        default=list,
    )
    anio = serializers.IntegerField(min_value=2000)
    mes = serializers.IntegerField(min_value=1, max_value=12)
    tipo_cobro = serializers.ChoiceField(
        choices=[Cobro.TIPO_MENSUAL, Cobro.TIPO_DIA_CANCHA],
        required=False,
        default=Cobro.TIPO_MENSUAL,
    )
    monto_cuota = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    monto_pagado = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=False,
        default=0,
    )
    fecha_registro_pago = serializers.DateField(required=False, allow_null=True)
    metodo_pago = serializers.CharField(required=False, allow_blank=True, default="")
    observaciones = serializers.CharField(required=False, allow_blank=True, default="")
    actualizar_existentes = serializers.BooleanField(required=False, default=False)
    usar_todos_los_socios = serializers.BooleanField(required=False, default=False)
    marcar_todos_como_usuarios_socio = serializers.BooleanField(required=False, default=False)


class PagoSerializer(serializers.ModelSerializer):
    socio_id = serializers.PrimaryKeyRelatedField(
        queryset=Socio.objects.all(),
        source="socio",
        required=False,
        allow_null=True,
    )
    socio_nombre = serializers.SerializerMethodField()
    alumno_nombre = serializers.SerializerMethodField()
    profesor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = [
            "id",
            "tipo",
            "monto",
            "fecha_pago",
            "mes",
            "anio",
            "socio_id",
            "alumno_id",
            "profesor_id",
            "metodo_pago",
            "observaciones",
            "socio_nombre",
            "alumno_nombre",
            "profesor_nombre",
        ]
        extra_kwargs = {
            "alumno_id": {"required": False, "allow_null": True},
            "profesor_id": {"required": False, "allow_null": True},
            "metodo_pago": {"required": False, "allow_blank": True},
            "observaciones": {"required": False, "allow_blank": True},
        }

    def get_socio_nombre(self, obj):
        if not obj.socio:
            return ""
        return f"{obj.socio.apellido}, {obj.socio.nombre}".strip(", ")

    def get_alumno_nombre(self, obj):
        return ""

    def get_profesor_nombre(self, obj):
        return ""


class PagosPaginatedResponseSerializer(serializers.Serializer):
    items = PagoSerializer(many=True)
    total_pages = serializers.IntegerField(min_value=1)
    total_count = serializers.IntegerField(min_value=0)
    page_size = serializers.IntegerField(min_value=1)


class MovimientoFinancieroSerializer(serializers.ModelSerializer):
    mes = serializers.SerializerMethodField()
    anio = serializers.SerializerMethodField()

    class Meta:
        model = MovimientoFinanciero
        fields = [
            "id",
            "tipo",
            "fecha",
            "mes",
            "anio",
            "grupo",
            "rubro",
            "concepto",
            "monto",
            "metodo",
            "observaciones",
        ]
        extra_kwargs = {
            "metodo": {"required": False, "allow_blank": True},
            "observaciones": {"required": False, "allow_blank": True},
        }

    def get_mes(self, obj):
        return obj.fecha.month

    def get_anio(self, obj):
        return obj.fecha.year


class MovimientosFinancierosPaginatedResponseSerializer(serializers.Serializer):
    items = MovimientoFinancieroSerializer(many=True)
    total_pages = serializers.IntegerField(min_value=1)
    total_count = serializers.IntegerField(min_value=0)
    page_size = serializers.IntegerField(min_value=1)