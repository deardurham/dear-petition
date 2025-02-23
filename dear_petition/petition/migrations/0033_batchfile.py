# Generated by Django 2.2.13 on 2020-08-02 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("petition", "0032_auto_20200709_1834"),
    ]

    operations = [
        migrations.CreateModel(
            name="BatchFile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_uploaded", models.DateTimeField(auto_now_add=True)),
                ("file", models.FileField(upload_to="ciprs/")),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="petition.Batch",
                    ),
                ),
            ],
        ),
    ]
