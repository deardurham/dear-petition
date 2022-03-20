import pytest

from dear_petition.petition import constants
from dear_petition.petition.models import Batch
from dear_petition.petition.etl.load import (
    create_batch_petitions,
    create_petitions_from_records,
    import_ciprs_records,
)
from dear_petition.petition.tests.factories import (
    OffenseFactory,
    OffenseRecordFactory,
    PetitionFactory,
    CIPRSRecordFactory,
)
from dear_petition.petition.etl.load import link_offense_records
from dear_petition.petition.etl.transform import recalculate_petitions

pytestmark = pytest.mark.django_db


def test_recalculate_petitions(petition):
    petition = PetitionFactory(form_type=constants.UNDERAGED_CONVICTIONS)
    batch = petition.batch
    record = CIPRSRecordFactory(
        batch=batch, jurisdiction=constants.DISTRICT_COURT, county="DURHAM"
    )
    offense = OffenseFactory(
        disposition_method="PROBATION OTHER",
        ciprs_record=record,
        jurisdiction=constants.DISTRICT_COURT,
    )
    offense_record_ids = []
    for i in range(12):
        offense_record = OffenseRecordFactory(offense=offense, action="CHARGED")
        petition.offense_records.add(offense_record)
        if len(offense_record_ids) < 5:
            offense_record_ids.append(offense_record.id)
    link_offense_records(petition)

    assert (
        petition.offense_records.filter(petitionoffenserecord__active=True).count()
        == 12
    )
    assert petition.has_attachments()
    recalculate_petitions(petition.id, offense_record_ids)
    assert (
        petition.offense_records.filter(petitionoffenserecord__active=True).count() == 5
    )
    assert not petition.has_attachments()
