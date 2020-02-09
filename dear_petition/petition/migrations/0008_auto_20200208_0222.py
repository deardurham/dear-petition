# Generated by Django 2.2.4 on 2020-02-08 02:22

from django.db import migrations


def move_batch_fks(apps, schema_editor):
    Batch = apps.get_model("petition", "Batch")
    for batch in Batch.objects.all():
        print(f"Adding batch {batch.pk} to {batch.records.count()} records")
        batch.records.update(batch=batch)


class Migration(migrations.Migration):

    dependencies = [
        ("petition", "0007_auto_20200208_0221"),
    ]

    operations = [migrations.RunPython(move_batch_fks)]
