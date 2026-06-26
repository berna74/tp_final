from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socios", "0007_pago"),
    ]

    operations = [
        migrations.AddField(
            model_name="cobro",
            name="marcar_en_rojo",
            field=models.BooleanField(default=False),
        ),
    ]
