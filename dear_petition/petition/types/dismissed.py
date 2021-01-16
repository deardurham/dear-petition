from django.db.models import Q

from dear_petition.petition.models import OffenseRecord
from dear_petition.petition.constants import DISMISSED_DISPOSITION_METHODS


def get_offense_records(batch, jurisdiction=""):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if jurisdiction:
        qs = qs.filter(offense__ciprs_record__jurisdiction=jurisdiction)
    qs = qs.filter(build_query())
    return qs.select_related("offense__ciprs_record__batch")


def build_query():
    action = Q(action="CHARGED")
    methods = Q()
    for method in DISMISSED_DISPOSITION_METHODS:
        methods |= Q(offense__disposition_method__iexact=method)
    guilty_to_lesser = build_guilty_to_lesser_query()
    query = action & methods | guilty_to_lesser
    return query


def build_guilty_to_lesser_query():
    action = Q(action="CHARGED")
    method = Q(offense__disposition_method="DISPOSED BY JUDGE")
    plea = Q(offense__plea="GUILTY TO LESSER")
    query = action & method & plea
    return query


def dismissed_query():
    action = Q(action="CHARGED")
    methods = Q()
    for method in DISMISSED_DISPOSITION_METHODS:
        methods |= Q(offense__disposition_method__iexact=method)
    return action & methods


def same_day_conviction(batch, jurisdiction):
    """
    Logic:
        I was charged with multiple offenses, and while the charges listed above were
        dismissed, the following charges resulted in a conviction on the day of the
        dismissal or had not yet reached final disposition.
    """
    qs = OffenseRecord.objects.filter(
        offense__ciprs_record__batch=batch,
        offense__ciprs_record__jurisdiction=jurisdiction,
    )
    offenses = []
    for record in batch.records.all():
        dismissed = qs.filter(dismissed_query())
        guilty = qs.filter(offense__verdict="GUILTY")
        if dismissed.exists() and guilty.exists():
            offenses.append(guilty.first())
    return offenses
