import os
from typing import List
from django.db import transaction
import tablib

from dear_petition.petition import models as pm
from dear_petition.petition import resources as pr

from .load import create_batch_petitions, create_documents, assign_agencies_to_documents


def recalculate_petitions(petition_id, offense_record_ids):
    petition = pm.Petition.objects.get(id=petition_id)

    with transaction.atomic():
        pm.PetitionOffenseRecord.objects.filter(petition_id=petition.id).update(
            active=False
        )
        pm.PetitionOffenseRecord.objects.filter(
            petition_id=petition.id, offense_record_id__in=offense_record_ids
        ).update(active=True)
        create_documents(petition)
        petition = assign_agencies_to_documents(petition)

    return petition


def combine_batches(batch_ids: List[int], label: str, user_id: int):

    client_resource = pr.ClientResource()
    record_resource = pr.RecordResource()
    offense_resource = pr.OffenseResource()
    offense_record_resource = pr.OffenseRecordResource()

    with transaction.atomic():
        new_batch = pm.Batch.objects.create(label=label, user_id=user_id)
        batches = pm.Batch.objects.filter(id__in=batch_ids)

        saved_file_nos = []
        saved_batch_files = {}
        for batch in batches:
            for record in batch.records.iterator():

                if record.file_no in saved_file_nos:
                    continue # Duplicate record of one already imported

                if record.batch_file:
                    file = record.batch_file.file.file
                    file_name = os.path.basename(file.name)
                    
                    if saved_batch_files.get(file_name):
                        new_batch_file = saved_batch_files[file_name]
                    else:
                        file.name = file_name
                        new_batch_file = new_batch.files.create(file=file)
                        saved_batch_files[file_name] = new_batch_file
                else:
                    new_batch_file=None

                export_record_dataset = record_resource.export(queryset=pm.CIPRSRecord.objects.filter(id=record.id))
                import_record_dataset = tablib.Dataset()
                import_record_dataset.headers = [col.column_name for col in record_resource.get_import_fields()]
                import_record_dataset.append([new_batch.id] + [value if value else None for value in export_record_dataset[0]])
                record_resource.import_data(import_record_dataset)
                record_id = record_resource.saved_instance_ids[-1]

                if new_batch_file:
                    new_record = pm.CIPRSRecord.objects.get(id=record_id)
                    new_record.batch_file = new_batch_file
                    new_record.save()

                for offense in record.offenses.all():
                    export_offense_dataset = offense_resource.export(queryset=pm.Offense.objects.filter(id=offense.id))
                    import_offense_dataset = tablib.Dataset()
                    import_offense_dataset.headers = [col.column_name for col in offense_resource.get_import_fields()]
                    import_offense_dataset.append([record_id] + [value if value else None for value in export_offense_dataset[0]])
                    offense_resource.import_data(import_offense_dataset)
                    offense_id = offense_resource.saved_instance_ids[-1]

                    export_offense_record_dataset = offense_record_resource.export(queryset=pm.OffenseRecord.objects.filter(offense_id=offense.id))
                    import_offense_record_dataset = tablib.Dataset()
                    import_offense_record_dataset.headers = [col.column_name for col in offense_record_resource.get_import_fields()]
                    for row in export_offense_record_dataset.dict:
                        import_offense_record_dataset.append([offense_id] + [value if value else None for value in row.values()])

                    offense_record_resource.import_data(import_offense_record_dataset)

                saved_file_nos.append(record.file_no)
        
        create_batch_petitions(new_batch)

        return new_batch
