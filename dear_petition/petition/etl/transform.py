from django.db import transaction
from django.db.models import Q

from dear_petition.petition import models as pm
from dear_petition.petition.constants import ATTACHMENT

from .load import create_documents, assign_agencies_to_documents


def recalculate_petitions(petition_id, offense_record_ids):
    petition = pm.Petition.objects.get(id=petition_id)

    with transaction.atomic():
        pm.PetitionOffenseRecord.objects.filter(petition_id=petition.id).update(
            active=False
        )
        pm.PetitionOffenseRecord.objects.filter(
            petition_id=petition.id, offense_record_id__in=offense_record_ids
        ).update(active=True)
        pm.PetitionDocument.objects.filter(petition=petition).delete()
        create_documents(petition)
        petition = assign_agencies_to_documents(petition)

    return petition
