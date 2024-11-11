import logging
from dateutil.relativedelta import relativedelta

from django.utils import timezone
from django.db.models import Q

from dear_petition.petition.constants import PORTAL_DISPOSITION_METHODS_CONVICTED
from dear_petition.petition.models import OffenseRecord
from dear_petition.petition import constants as pc

logger = logging.getLogger(__name__)


def get_offense_records(batch, jurisdiction=""):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if jurisdiction:
        qs = qs.filter(offense__jurisdiction=jurisdiction)
    query = build_query()
    qs = qs.filter(query)
    return qs.select_related("offense__ciprs_record__batch")


def build_query():
    action = Q(action=pc.CONVICTED)
    severity = Q(severity__iexact=pc.SEVERITIES.FELONY)
    today = timezone.now().date()
    waiting_period_start_date = today - relativedelta(years=10)
    waiting_period = Q(offense__disposed_on__lt=waiting_period_start_date)
    adult_felony_ciprs = action & severity & waiting_period

    methods = Q()
    for method in PORTAL_DISPOSITION_METHODS_CONVICTED:
        methods |= Q(offense__disposition_method__iexact=method)
    adult_felony_portal = methods & severity & waiting_period

    return adult_felony_ciprs | adult_felony_portal

