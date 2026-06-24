from rest_framework import serializers

from .models import Cobro, Socio


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
            "monto_cuota",
            "monto_pagado",
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
    anio = serializers.IntegerField(min_value=2000)
    mes = serializers.IntegerField(min_value=1, max_value=12)
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