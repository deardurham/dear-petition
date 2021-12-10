from django.db import transaction

from dear_petition.petition import models as pm
from dear_petition.petition.constants import ATTACHMENT
from .load import link_offense_records_and_attachments


def recalculate_petitions(petition_id, offense_record_ids):
    petition = pm.Petition.objects.get(id=petition_id)
    assert (
        petition.form_type != ATTACHMENT
    ), "These are the ones that are supposed to get attached, not attached to"
    offense_records = pm.OffenseRecord.objects.filter(id__in=offense_record_ids)

    with transaction.atomic():
        petition.get_all_offense_records(include_annotations=False).update(active=False)
        offense_records.update(active=True)
        petition.attachments.all().delete()
        link_offense_records_and_attachments(petition)

    return petition
