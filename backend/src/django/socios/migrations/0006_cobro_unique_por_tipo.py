from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socios", "0005_cobro_tipo_cobro"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="cobro",
            name="unique_cobro_periodo_por_socio",
        ),
        migrations.AddConstraint(
            model_name="cobro",
            constraint=models.UniqueConstraint(
                fields=("socio", "anio", "mes", "tipo_cobro"),
                name="unique_cobro_periodo_tipo_por_socio",
            ),
        ),
    ]
