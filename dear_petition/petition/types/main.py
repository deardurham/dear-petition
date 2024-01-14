import logging

from django.db.models import F

from dear_petition.petition.types import (
    dismissed,
    not_guilty,
    underaged_convictions,
    adult_felonies,
    adult_misdemeanors,
)
from dear_petition.petition import constants


logger = logging.getLogger(__name__)
TYPE_MAP = {
    constants.DISMISSED: dismissed.get_offense_records,
    constants.NOT_GUILTY: not_guilty.get_offense_records,
    constants.UNDERAGED_CONVICTIONS: underaged_convictions.get_offense_records,
    constants.ADULT_FELONIES: adult_felonies.get_offense_records,
    constants.ADULT_MISDEMEANORS: adult_misdemeanors.get_offense_records,
}


def petition_offense_records(batch, petition_type, jurisdiction=""):
    get_offense_records = TYPE_MAP.get(petition_type)
    qs = get_offense_records(batch, jurisdiction)
    return qs


def identify_distinct_petitions(offense_records):
    qs = offense_records.values(
        "offense__ciprs_record__jurisdiction", "offense__ciprs_record__county"
    )
    qs = qs.values(
        jurisdiction=F("offense__ciprs_record__jurisdiction"),
        county=F("offense__ciprs_record__county"),
    ).distinct()
    logger.info(f"Distinct petitions: {list(qs.values_list('county', 'jurisdiction'))}")
    return qs
