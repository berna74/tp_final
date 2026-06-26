from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("socios", "0006_cobro_unique_por_tipo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pago",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("Cuota Social", "Cuota Social"),
                            ("Abono Mensual", "Abono Mensual"),
                            ("Abono Diario", "Abono Diario"),
                            ("Clase", "Clase"),
                        ],
                        default="Abono Mensual",
                        max_length=30,
                    ),
                ),
                ("monto", models.DecimalField(decimal_places=2, max_digits=10)),
                ("fecha_pago", models.DateField()),
                ("mes", models.IntegerField()),
                ("anio", models.IntegerField()),
                ("alumno_id", models.IntegerField(blank=True, null=True)),
                ("profesor_id", models.IntegerField(blank=True, null=True)),
                ("metodo_pago", models.CharField(blank=True, default="", max_length=50)),
                ("observaciones", models.TextField(blank=True, default="")),
                (
                    "socio",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="pagos",
                        to="socios.socio",
                    ),
                ),
            ],
            options={
                "db_table": "PAGOS",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("socio", "anio", "mes", "tipo"),
                        name="unique_pago_periodo_tipo_por_socio",
                    )
                ],
            },
        ),
    ]
