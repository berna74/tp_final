from django.db import models


class Socio(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_inscripcion = models.DateField(null=True, blank=True)
    profesor_id = models.IntegerField(null=True, blank=True, db_column="profesor_id")
    registra_deuda = models.BooleanField(default=False)

    class Meta:
        db_table = "SOCIOS"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
