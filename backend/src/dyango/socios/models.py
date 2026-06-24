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


class Cobro(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="cobros")
    anio = models.IntegerField()
    mes = models.IntegerField()
    monto_cuota = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_registro_pago = models.DateField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")

    class Meta:
        db_table = "COBROS"
        constraints = [
            models.UniqueConstraint(
                fields=["socio", "anio", "mes"],
                name="unique_cobro_periodo_por_socio",
            )
        ]

    def __str__(self):
        return f"Cobro {self.socio_id} - {self.mes}/{self.anio}"
