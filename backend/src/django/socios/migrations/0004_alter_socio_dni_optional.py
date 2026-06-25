from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socios", "0003_cobro"),
    ]

    operations = [
        migrations.AlterField(
            model_name="socio",
            name="dni",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
    ]
