# Generated by Django 3.2.13 on 2022-10-16 19:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sendgrid", "0002_alter_attachment_content_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="spam_score",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
