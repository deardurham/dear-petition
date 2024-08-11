import os
from typing import List
from django.db import transaction

from dear_petition.petition import models as pm

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

    with transaction.atomic():
        new_batch = pm.Batch.objects.create(label=label, user_id=user_id)
        batches = pm.Batch.objects.filter(id__in=batch_ids)

        saved_file_nos = []
        saved_batch_files = {}
        for batch in batches:
            for record in batch.records.iterator():

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

                new_record = new_batch.records.create(batch=new_batch, batch_file=new_batch_file, data=record.data)
                # Pass file numbers of CIPRS records that have already been saved in this batch of CIPRS records.
                # If this CIPRS record is in the list, it will not be saved again.
                new_record.refresh_record_from_data(saved_file_nos)
                saved_file_nos.append(record.file_no)
        
        create_batch_petitions(new_batch)

        return new_batch
