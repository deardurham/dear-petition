import logging
from dateutil.relativedelta import relativedelta

from django.utils import timezone
from django.db.models import Q

from dear_petition.petition.models import OffenseRecord
from dear_petition.petition import constants as pc
from dear_petition.petition.utils import resolve_dob

logger = logging.getLogger(__name__)


def get_offense_records(batch, jurisdiction=""):
    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if jurisdiction:
        qs = qs.filter(offense__ciprs_record__jurisdiction=jurisdiction)
    dob = resolve_dob(qs)
    if not dob:
        return qs  # We can't determine this petition type without the date of birth
    query = build_query(dob)
    qs = qs.filter(query)
    return qs.select_related("offense__ciprs_record__batch")


def build_query(dob):
    action = Q(action=pc.CONVICTED)
    verdict = Q(severity__iexact=pc.SEVERITIES.FELONY)
    today = timezone.now().date()
    waiting_period_start_date = today - relativedelta(years=10)
    waiting_period = Q(offense__disposed_on__lt=waiting_period_start_date)
    query = action & verdict & waiting_period
    return query
