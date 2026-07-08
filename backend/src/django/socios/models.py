from django.db import models


class Socio(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, blank=True, default="")
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
    TIPO_MENSUAL = "mensual"
    TIPO_DIA_CANCHA = "dia_cancha"
    TIPOS_COBRO = [
        (TIPO_MENSUAL, "Mensual"),
        (TIPO_DIA_CANCHA, "Dia de cancha"),
    ]

    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="cobros")
    anio = models.IntegerField()
    mes = models.IntegerField()
    tipo_cobro = models.CharField(max_length=20, choices=TIPOS_COBRO, default=TIPO_MENSUAL)
    monto_cuota = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    marcar_en_rojo = models.BooleanField(default=False)
    fecha_registro_pago = models.DateField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")

    class Meta:
        db_table = "COBROS"
        constraints = [
            models.UniqueConstraint(
                fields=["socio", "anio", "mes", "tipo_cobro"],
                name="unique_cobro_periodo_tipo_por_socio",
            )
        ]

    def __str__(self):
        return f"Cobro {self.socio_id} - {self.mes}/{self.anio}"


class Pago(models.Model):
    TIPO_CUOTA_SOCIAL = "Cuota Social"
    TIPO_ABONO_MENSUAL = "Abono Mensual"
    TIPO_ABONO_DIARIO = "Abono Diario"
    TIPO_CLASE = "Clase"
    TIPOS_PAGO = [
        (TIPO_CUOTA_SOCIAL, "Cuota Social"),
        (TIPO_ABONO_MENSUAL, "Abono Mensual"),
        (TIPO_ABONO_DIARIO, "Abono Diario"),
        (TIPO_CLASE, "Clase"),
    ]

    tipo = models.CharField(max_length=30, choices=TIPOS_PAGO, default=TIPO_ABONO_MENSUAL)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    mes = models.IntegerField()
    anio = models.IntegerField()
    socio = models.ForeignKey(
        Socio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pagos",
    )
    alumno_id = models.IntegerField(null=True, blank=True)
    profesor_id = models.IntegerField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")

    class Meta:
        db_table = "PAGOS"
        constraints = [
            models.UniqueConstraint(
                fields=["socio", "anio", "mes", "tipo"],
                name="unique_pago_periodo_tipo_por_socio",
            )
        ]

    def __str__(self):
        return f"Pago {self.id} - {self.tipo} {self.mes}/{self.anio}"


class MovimientoFinanciero(models.Model):
    TIPO_INGRESO = "ingreso"
    TIPO_GASTO = "gasto"
    TIPOS_MOVIMIENTO = [
        (TIPO_INGRESO, "Ingreso"),
        (TIPO_GASTO, "Gasto"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    fecha = models.DateField()
    grupo = models.CharField(max_length=80)
    rubro = models.CharField(max_length=120)
    concepto = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    metodo = models.CharField(max_length=50, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "MOVIMIENTOS_FINANCIEROS"
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.tipo} {self.rubro} {self.fecha}"
