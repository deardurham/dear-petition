import pytest

from dear_petition.petition.etl.paginator import OffenseRecordPaginator
from dear_petition.petition.tests.factories import OffenseRecordFactory


pytestmark = pytest.mark.django_db


def test_attachment_page(batch, petition, offense1):
    for i in range(20):
        offense_record = OffenseRecordFactory(offense=offense1)
        petition.offense_records.add(offense_record)
    paginator = OffenseRecordPaginator(petition)
    assert len(paginator.petition_offense_records()) == 10
    has_attachment = None
    for attachment_records in paginator.attachment_offense_records():
        has_attachment = True
        assert len(attachment_records) == 10
    assert has_attachment
