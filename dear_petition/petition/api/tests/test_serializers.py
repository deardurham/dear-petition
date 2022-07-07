import pytest

from dear_petition.petition.api.serializers import OffenseRecordSerializer
from dear_petition.petition.tests.factories import OffenseRecordFactory


@pytest.mark.django_db
class TestOffenseRecordSerializer:
    def test_offense_date(self):
        record = OffenseRecordFactory()
        serializer = OffenseRecordSerializer(record)
        assert (
            serializer.data["offense_date"]
            == record.offense.ciprs_record.offense_date.date()
        )

    def test_offense_date_none(self):
        record = OffenseRecordFactory(offense__ciprs_record__offense_date=None)
        serializer = OffenseRecordSerializer(record)
        assert serializer.data["offense_date"] is None
