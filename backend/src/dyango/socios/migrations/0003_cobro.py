# Generated manually for Cobros module

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("socios", "0002_create_role_groups"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cobro",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("anio", models.IntegerField()),
                ("mes", models.IntegerField()),
                ("monto_cuota", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "monto_pagado",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("fecha_registro_pago", models.DateField(blank=True, null=True)),
                ("metodo_pago", models.CharField(blank=True, default="", max_length=50)),
                ("observaciones", models.TextField(blank=True, default="")),
                (
                    "socio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cobros",
                        to="socios.socio",
                    ),
                ),
            ],
            options={
                "db_table": "COBROS",
            },
        ),
        migrations.AddConstraint(
            model_name="cobro",
            constraint=models.UniqueConstraint(
                fields=("socio", "anio", "mes"),
                name="unique_cobro_periodo_por_socio",
            ),
        ),
    ]
