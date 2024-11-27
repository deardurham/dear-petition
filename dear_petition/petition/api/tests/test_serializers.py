from datetime import timedelta, datetime

import pytest
from dear_petition.petition.api.serializers import (
    AdultFelonyOffenseRecordSerializer,
    AdultMisdemeanorOffenseRecordSerializer,
    DismissedOffenseRecordSerializer,
    NotGuiltyOffenseRecordSerializer,
    OffenseRecordSerializer,
    UnderagedConvictionOffenseRecordSerializer,
)
from dear_petition.petition.tests.factories import OffenseRecordFactory
import dear_petition.petition.constants as pc


@pytest.mark.django_db
class TestOffenseRecordSerializer:
    def test_offense_date(self):
        record = OffenseRecordFactory()
        serializer = OffenseRecordSerializer(record)
        assert serializer.data["offense_date"] == record.offense.ciprs_record.offense_date.date()

    def test_offense_date_none(self):
        record = OffenseRecordFactory(offense__ciprs_record__offense_date=None)
        serializer = OffenseRecordSerializer(record)
        assert serializer.data["offense_date"] is None

    def test_dismissed_record_underaged_warning(self, charged_dismissed_record):
        charged_dismissed_record.offense.ciprs_record.dob = (
            charged_dismissed_record.offense.ciprs_record.offense_date.date()
            - timedelta(days=365 * 16)
        )
        charged_dismissed_record.offense.ciprs_record.save()

        serializer = DismissedOffenseRecordSerializer(charged_dismissed_record)
        assert serializer.data["warnings"] == [
            "This offense may be a candidate for the AOC-CR-293 petition form"
        ]

    def test_not_guilty_underaged_warning(self, charged_not_guilty_record):
        charged_not_guilty_record.offense.ciprs_record.dob = (
            charged_not_guilty_record.offense.ciprs_record.offense_date.date()
            - timedelta(days=365 * 16)
        )
        charged_not_guilty_record.offense.ciprs_record.save()

        serializer = NotGuiltyOffenseRecordSerializer(charged_not_guilty_record)
        assert serializer.data["warnings"] == [
            "This offense may be a candidate for the AOC-CR-293 petition form"
        ]

    def test_underaged_conviction_assault_warning(self, record1, non_dismissed_offense):
        record1.dob = datetime(2000, 1, 2)
        record1.offense_date = datetime(2018, 1, 1)
        record1.save()

        offense_record = OffenseRecordFactory(
            action="CONVICTED", description="Assault", offense=non_dismissed_offense
        )
        serializer = UnderagedConvictionOffenseRecordSerializer(offense_record)
        assert serializer.data["warnings"] == ["This is an assault conviction"]

    def test_adult_felony_assault_warning(self, record1, non_dismissed_offense):
        record1.dob = datetime(2000, 1, 2)
        record1.offense_date = datetime(2019, 1, 1)
        record1.save()

        offense_record = OffenseRecordFactory(
            action="CONVICTED",
            description="Assault",
            severity=pc.SEVERITY_FELONY,
            offense=non_dismissed_offense,
        )
        serializer = AdultFelonyOffenseRecordSerializer(offense_record)
        assert serializer.data["warnings"] == ["This is an assault conviction"]

    def test_adult_misdemeanor_assault_warning(self, record1, non_dismissed_offense):
        record1.dob = datetime(2000, 1, 2)
        record1.offense_date = datetime(2019, 1, 1)
        record1.save()

        offense_record = OffenseRecordFactory(
            action="CONVICTED",
            description="Assault",
            severity=pc.SEVERITY_MISDEMEANOR,
            offense=non_dismissed_offense,
        )
        serializer = AdultFelonyOffenseRecordSerializer(offense_record)
        assert serializer.data["warnings"] == ["This is an assault conviction"]
