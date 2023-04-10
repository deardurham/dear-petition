from django.db.models import Q

from dear_petition.petition import constants as pc
from dear_petition.petition.models import OffenseRecord


def get_offense_records(petition):
    """
    Offense records flagged for Addendum 3B are those offense records that present on CIPRS records that have offenses we are trying to expunge,
    but can not be expunged themselves because they either led to a conviction or have not yet been disposed.
    """

    active_records = petition.offense_records.filter(petitionoffenserecord__active=True)
    active_ciprs_records = active_records.values("offense__ciprs_record").distinct()
    active_record_ids = active_records.values_list("id")

    return OffenseRecord.objects.filter(
        ~Q(id__in=active_record_ids),
        offense__ciprs_record__in=active_ciprs_records,
        action=pc.CONVICTED,
        offense__verdict=pc.GUILTY,
    )
