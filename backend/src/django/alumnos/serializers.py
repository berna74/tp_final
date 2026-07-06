from rest_framework import serializers

from profesores.models import Profesor

from .models import Alumno


class ProfesorBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ["id", "nombre", "apellido"]


class AlumnoSerializer(serializers.ModelSerializer):
    profesor = ProfesorBriefSerializer(read_only=True)
    profesor_id = serializers.PrimaryKeyRelatedField(
        queryset=Profesor.objects.all(),
        source="profesor",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Alumno
        fields = [
            "id",
            "nombre",
            "apellido",
            "dni",
            "email",
            "telefono",
            "fecha_inscripcion",
            "profesor",
            "profesor_id",
            "nivel",
            "activo",
        ]
        extra_kwargs = {
            "nombre": {"required": False, "allow_blank": True},
            "apellido": {"required": False, "allow_blank": True},
            "dni": {"required": False, "allow_blank": True},
            "email": {"required": False, "allow_blank": True},
            "telefono": {"required": False, "allow_blank": True},
            "fecha_inscripcion": {"required": False, "allow_null": True},
            "nivel": {"required": False, "allow_blank": True},
            "activo": {"required": False},
        }

    def create(self, validated_data):
        validated_data.setdefault("nombre", "")
        validated_data.setdefault("apellido", "")
        validated_data.setdefault("dni", "")
        validated_data.setdefault("email", "")
        validated_data.setdefault("telefono", "")
        validated_data.setdefault("nivel", "")
        validated_data.setdefault("activo", True)
        return super().create(validated_data)
