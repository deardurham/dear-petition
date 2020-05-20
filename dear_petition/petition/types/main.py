from dear_petition.petition.types import dismissed
from dear_petition.petition import constants


TYPE_MAP = {
    constants.DISMISSED: dismissed.get_offense_records,
}


def petition_offense_records(batch, petition_type):
    offense_records = TYPE_MAP.get(petition_type)
    return offense_records(batch)
