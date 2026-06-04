from rest_framework import serializers

from .models import Socio


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