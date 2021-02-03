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


def same_day_convictions(dismissed_records):
    """
    To support field 3(b) on the AOC-CR-287 form, return a list of guilty
    OffenseRecords that also had dismissals on the same day.

    Petition language:
        I was charged with multiple offenses, and while the charges
        listed above were dismissed, the following charges resulted in a
        conviction on the day of the dismissal or had not yet reached final
        disposition.
    """
    dismissed_record_ids = dismissed_records.values_list("id", flat=True)
    qs = (
        OffenseRecord.objects.filter(pk__in=list(dismissed_record_ids))
        .values_list("offense__ciprs_record", "offense__disposed_on")
        .distinct()
    )
    records = []
    for ciprs_record_id, disposed_on in qs:
        guilty_records = OffenseRecord.objects.filter(
            offense__verdict="GUILTY",
            offense__ciprs_record__id=ciprs_record_id,
            offense__disposed_on=disposed_on,
            action="CONVICTED",
        )
        if guilty_records.exists():
            records.extend(
                guilty_records.select_related("offense__ciprs_record__batch")
            )
    return records
