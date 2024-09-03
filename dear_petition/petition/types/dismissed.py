from django.db.models import Q

from dear_petition.petition.models import OffenseRecord
from dear_petition.petition.constants import CIPRS_DISPOSITION_METHODS_DISMISSED, PORTAL_DISPOSITION_METHODS_DISMISSED


def get_offense_records(batch, jurisdiction=""):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if jurisdiction:
        qs = qs.filter(offense__ciprs_record__jurisdiction=jurisdiction)
    qs = qs.filter(build_query()).exclude(severity="INFRACTION")
    return qs.select_related("offense__ciprs_record__batch")


def build_query():
    action = Q(action="CHARGED")
    
    methods_ciprs = Q()
    for method in CIPRS_DISPOSITION_METHODS_DISMISSED:
        methods_ciprs |= Q(offense__disposition_method__iexact=method)
    dismissed_ciprs = action & methods_ciprs

    methods_portal = Q()
    for method in PORTAL_DISPOSITION_METHODS_DISMISSED:
        methods_portal |= Q(offense__disposition_method__iexact=method)
    dismissed_portal = methods_portal

    return dismissed_ciprs | dismissed_portal
