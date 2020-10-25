import logging

from django.db.models import F

from dear_petition.petition.types import dismissed, not_guilty
from dear_petition.petition import constants


logger = logging.getLogger(__name__)
TYPE_MAP = {
    constants.DISMISSED: dismissed.get_offense_records,
    constants.NOT_GUILTY: not_guilty.get_offense_records,
}


def petition_offense_records(batch, petition_type, jurisdiction=""):
    get_offense_records = TYPE_MAP.get(petition_type)
    qs = get_offense_records(batch, jurisdiction)
    logger.info(f"{petition_type} records: {qs}")
    return qs


def identify_distinct_petitions(offense_records):
    qs = offense_records.values(
        "offense__ciprs_record__jurisdiction", "offense__ciprs_record__county"
    )
    qs = qs.values(
        jurisdiction=F("offense__ciprs_record__jurisdiction"),
        county=F("offense__ciprs_record__county"),
    ).distinct()
    logger.info(f"Distinct petitions: {qs}")
    return qs
