from django.db.models import F

from dear_petition.petition.types import dismissed
from dear_petition.petition import constants


TYPE_MAP = {
    constants.DISMISSED: dismissed.get_offense_records,
}


def petition_offense_records(batch, petition_type, jurisdiction=""):
    get_offense_records = TYPE_MAP.get(petition_type)
    return get_offense_records(batch, jurisdiction)


def identify_distinct_petitions(offense_records):
    qs = offense_records.values(
        "offense__ciprs_record__jurisdiction", "offense__ciprs_record__county"
    )
    return qs.values(
        jurisdiction=F("offense__ciprs_record__jurisdiction"),
        county=F("offense__ciprs_record__county"),
    )
