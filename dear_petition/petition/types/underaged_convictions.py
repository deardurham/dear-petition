import logging
from dateutil.relativedelta import relativedelta

from django.db.models import Q

from dear_petition.petition.models import OffenseRecord
from dear_petition.petition.types.dismissed import build_query as build_dismissed_query
from dear_petition.petition.types.not_guilty import (
    build_query as build_not_guilty_query,
)
from dear_petition.petition.utils import resolve_dob_from_offense_records

logger = logging.getLogger(__name__)


def get_offense_records(batch, jurisdiction=""):

    qs = OffenseRecord.objects.filter(offense__ciprs_record__batch=batch)
    if not qs.exists():
        return qs

    if batch.client and batch.client.dob:
        dob = batch.client.dob
    else:
        dob = resolve_dob_from_offense_records(qs)
    if not dob:
        return OffenseRecord.objects.none()  # We can't determine this petition type without the date of birth

    if jurisdiction:
        qs = qs.filter(offense__ciprs_record__jurisdiction=jurisdiction)

    query = build_query(dob)
    qs = qs.filter(query).exclude(severity="INFRACTION")

    return qs


def build_query(dob):
    eighteenth_birthday = dob + relativedelta(years=18)
    logger.debug(f"Using {eighteenth_birthday} as eighteenth birthday (dob={dob})")
    dismissed_query = build_dismissed_query()
    not_guilty_query = build_not_guilty_query()
    before_eighteen = Q(offense__ciprs_record__offense_date__date__lt=eighteenth_birthday)
    query = before_eighteen & ~dismissed_query & ~not_guilty_query
    return query
