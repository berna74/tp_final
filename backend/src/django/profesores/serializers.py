from rest_framework import serializers

from socios.models import Socio

from .models import Profesor


class ProfesorSerializer(serializers.ModelSerializer):
    socio_id = serializers.PrimaryKeyRelatedField(
        source="socio",
        queryset=Socio.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Profesor
        fields = [
            "id",
            "nombre",
            "apellido",
            "dni",
            "email",
            "telefono",
            "horarios_clases",
            "socio_id",
        ]
        extra_kwargs = {
            "nombre": {"required": True, "allow_blank": False},
            "apellido": {"required": True, "allow_blank": False},
            "dni": {"required": False, "allow_blank": True},
            "email": {"required": False, "allow_blank": True},
            "telefono": {"required": False, "allow_blank": True},
            "horarios_clases": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        validated_data.setdefault("nombre", "")
        validated_data.setdefault("apellido", "")
        validated_data.setdefault("dni", "")
        validated_data.setdefault("email", "")
        validated_data.setdefault("telefono", "")
        validated_data.setdefault("horarios_clases", "")
        return super().create(validated_data)
