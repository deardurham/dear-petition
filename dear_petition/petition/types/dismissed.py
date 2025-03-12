from django.db.models import Q

from dear_petition.petition.models import OffenseRecord
from dear_petition.petition.constants import (
    CIPRS_DISPOSITION_METHODS_DISMISSED,
    PORTAL_DISPOSITION_METHODS_DISMISSED,
    SEVERITIES,
)


def get_offense_records(batch, jurisdiction=""):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if jurisdiction:
        qs = qs.filter(offense__jurisdiction=jurisdiction)
    qs = qs.filter(build_query())
    return qs.select_related("offense__ciprs_record__batch")


def build_query():
    action = Q(action="CHARGED")
    non_infraction = ~Q(severity=SEVERITIES.INFRACTION)
    eligible_infraction = Q(severity=SEVERITIES.INFRACTION) & Q(
        offense__ciprs_record__file_no__contains="CR"
    )

    methods_ciprs = Q()
    for method in CIPRS_DISPOSITION_METHODS_DISMISSED:
        methods_ciprs |= Q(offense__disposition_method__iexact=method)
    dismissed_ciprs = action & methods_ciprs & (non_infraction | eligible_infraction)

    methods_portal = Q()
    for method in PORTAL_DISPOSITION_METHODS_DISMISSED:
        methods_portal |= Q(offense__disposition_method__iexact=method)
    dismissed_portal = methods_portal & (non_infraction | eligible_infraction)

    return dismissed_ciprs | dismissed_portal
