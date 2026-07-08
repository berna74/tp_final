from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socios", "0008_cobro_marcar_en_rojo"),
    ]

    operations = [
        migrations.CreateModel(
            name="MovimientoFinanciero",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("ingreso", "Ingreso"), ("gasto", "Gasto")], max_length=20)),
                ("fecha", models.DateField()),
                ("grupo", models.CharField(max_length=80)),
                ("rubro", models.CharField(max_length=120)),
                ("concepto", models.CharField(max_length=150)),
                ("monto", models.DecimalField(decimal_places=2, max_digits=12)),
                ("metodo", models.CharField(blank=True, default="", max_length=50)),
                ("observaciones", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "MOVIMIENTOS_FINANCIEROS",
                "ordering": ["-fecha", "-id"],
            },
        ),
    ]