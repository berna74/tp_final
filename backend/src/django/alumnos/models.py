from django.db import models


class Alumno(models.Model):
    NIVEL_PRINCIPIANTE = "Principiante"
    NIVEL_INTERMEDIO = "Intermedio"
    NIVEL_AVANZADO = "Avanzado"
    NIVELES = [
        (NIVEL_PRINCIPIANTE, "Principiante"),
        (NIVEL_INTERMEDIO, "Intermedio"),
        (NIVEL_AVANZADO, "Avanzado"),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(max_length=100, blank=True, default="")
    telefono = models.CharField(max_length=20, blank=True, default="")
    fecha_inscripcion = models.DateField(null=True, blank=True)
    profesor = models.ForeignKey(
        "profesores.Profesor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alumnos",
    )
    nivel = models.CharField(max_length=20, blank=True, default="")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "ALUMNOS"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
