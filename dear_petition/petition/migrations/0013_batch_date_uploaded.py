# Generated by Django 2.2.4 on 2020-02-09 02:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("petition", "0012_auto_20200208_0240"),
    ]

    operations = [
        migrations.AddField(
            model_name="batch",
            name="date_uploaded",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
