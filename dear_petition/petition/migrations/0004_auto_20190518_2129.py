# Generated by Django 2.2 on 2019-05-18 21:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("petition", "0003_auto_20190518_1915")]

    operations = [
        migrations.AlterField(
            model_name="ciprsrecord",
            name="report_pdf",
            field=models.FileField(
                blank=True, null=True, upload_to="ciprs/", verbose_name="Report PDF"
            ),
        )
    ]
