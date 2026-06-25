from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socios", "0004_alter_socio_dni_optional"),
    ]

    operations = [
        migrations.AddField(
            model_name="cobro",
            name="tipo_cobro",
            field=models.CharField(
                choices=[("mensual", "Mensual"), ("dia_cancha", "Dia de cancha")],
                default="mensual",
                max_length=20,
            ),
        ),
    ]
