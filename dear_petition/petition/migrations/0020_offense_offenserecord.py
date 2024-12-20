# Generated by Django 2.2.10 on 2020-04-16 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("petition", "0019_auto_20200407_1720"),
    ]

    operations = [
        migrations.CreateModel(
            name="Offense",
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
                ("disposed_on", models.DateField(blank=True, null=True)),
                ("disposition_method", models.CharField(max_length=256)),
                (
                    "ciprs_record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offenses",
                        to="petition.CIPRSRecord",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OffenseRecord",
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
                ("law", models.CharField(blank=True, max_length=256)),
                ("code", models.IntegerField(blank=True, null=True)),
                ("action", models.CharField(max_length=256)),
                ("severity", models.CharField(max_length=256)),
                ("description", models.CharField(max_length=256)),
                (
                    "offense",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offense_records",
                        to="petition.Offense",
                    ),
                ),
            ],
        ),
    ]
