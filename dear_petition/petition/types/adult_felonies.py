from django.db.models import Q

from dear_petition.petition.models import OffenseRecord
from dear_petition.petition.types.dismissed import build_query as build_dismissed_query
from dear_petition.petition.types.not_guilty import (
    build_query as build_not_guilty_query,
)


def get_offense_records(batch, jurisdiction=""):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if jurisdiction:
        qs = qs.filter(offense__ciprs_record__jurisdiction=jurisdiction)
    query = build_query()
    qs = qs.filter(query)
    return qs.select_related("offense__ciprs_record__batch")


def build_query():
    action = Q(action="CONVICTED")
    verdict = Q(severity__iexact="FELONY")
    dismissed_query = build_dismissed_query()
    not_guilty_query = build_not_guilty_query()
    query = action & verdict & ~dismissed_query & ~not_guilty_query
    return query
