# Generated by Django 4.2.9 on 2024-09-17 03:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("petition", "0065_alter_ciprsrecord_arrest_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offense",
            name="plea",
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name="Plea"),
        ),
        migrations.AlterField(
            model_name="offense",
            name="verdict",
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name="Verdict"),
        ),
    ]
