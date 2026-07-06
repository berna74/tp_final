from django.db import models


class Profesor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(max_length=100, blank=True, default="")
    telefono = models.CharField(max_length=20, blank=True, default="")
    horarios_clases = models.TextField(blank=True, default="")
    socio = models.OneToOneField(
        "socios.Socio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profesor",
    )

    class Meta:
        db_table = "PROFESORES"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
