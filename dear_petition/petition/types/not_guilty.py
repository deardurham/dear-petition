from django.db.models import Q

from dear_petition.petition.constants import PORTAL_DISPOSITION_METHODS_NOT_GUILTY
from dear_petition.petition.models import OffenseRecord
from dear_petition.petition.types.dismissed import build_query as build_dismissed_query


def get_offense_records(batch, jurisdiction=""):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if jurisdiction:
        qs = qs.filter(offense__ciprs_record__jurisdiction=jurisdiction)
    query = build_query()
    qs = qs.filter(query).exclude(severity="INFRACTION")
    return qs.select_related("offense__ciprs_record__batch")


def build_query():
    action = Q(action="CHARGED")
    verdict = Q(offense__verdict__iexact="Not Guilty")
    dismissed_query = build_dismissed_query()
    not_guilty_ciprs = action & verdict & ~dismissed_query

    methods = Q()
    for method in PORTAL_DISPOSITION_METHODS_NOT_GUILTY:
        methods |= Q(offense__disposition_method__iexact=method)
    not_guilty_portal = methods

    return not_guilty_ciprs | not_guilty_portal
