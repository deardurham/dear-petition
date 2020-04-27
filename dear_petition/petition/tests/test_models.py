import pytest
import pytz
from django.conf import settings
from django.utils.timezone import localtime

from .factories import (
    BatchFactory,
    CIPRSRecordFactory,
    record_data,
)

from ..models import CIPRSRecord, OffenseRecord

from ..utils import (
    dt_obj_to_date,
    make_datetime_aware,
)

pytestmark = pytest.mark.django_db


def test_ciprs_record_create():
    """Test that the create_record queryset method

    This method should extract General, Case, and Defendant
    details from the data field on the CIPRSRecord instance and store that
    information in their fields
    """
    batch = BatchFactory()
    data = record_data(1)
    CIPRSRecord.objects.create_record(batch=batch, label=batch.label, data=data)
    ciprs_record = CIPRSRecord.objects.get(data=data)
    assert ciprs_record.batch == batch
    assert ciprs_record.label == batch.label
    assert ciprs_record.file_no == data["General"].get("File No", "")
    assert ciprs_record.county == data["General"].get("County", "")
    assert ciprs_record.dob.strftime("%Y-%m-%d") == data["Defendant"].get(
        "Date of Birth/Estimated Age", None
    )
    assert ciprs_record.sex == data["Defendant"].get("Sex", "")
    assert ciprs_record.race == data["Defendant"].get("Race", "")
    assert ciprs_record.case_status == data["Case Information"].get("Case Status", "")
    record_offense_date_str = ciprs_record.offense_date.astimezone(
        pytz.timezone(settings.TIME_ZONE)
    ).strftime("%Y-%m-%dT%H:%M:%S")
    data_offense_date_str = data.get("Case Information", {}).get("Offense Date", None)
    assert record_offense_date_str == data_offense_date_str
    data_arrest_date = data.get("Offense Record", {}).get("Arrest Date", "")
    if not data_arrest_date:
        data_arrest_date = dt_obj_to_date(ciprs_record.offense_date).strftime(
            "%Y-%m-%d"
        )
    assert ciprs_record.arrest_date.strftime("%Y-%m-%d") == data_arrest_date
    # Offense Assertions
    assert ciprs_record.offenses.first().disposed_on.strftime(
        "%Y-%m-%d"
    ) == ciprs_record.data.get("Offense Record").get("Disposed On")
    assert ciprs_record.offenses.first().disposition_method == ciprs_record.data.get(
        "Offense Record"
    ).get("Disposition Method")

    # OffenseRecord Assertions
    raw_data_actions = []
    raw_data_offense_records = ciprs_record.data.get("Offense Record").get("Records")
    for offense_record in raw_data_offense_records:
        for key, value in offense_record.items():
            if "Action" in key:
                raw_data_actions.extend(value)
    stored_actions = []
    stored_offense_records = list(ciprs_record.offenses.first().offense_records.all())
    for offense_record in stored_offense_records:
        stored_actions.extend(offense_record.action)

    assert len(stored_offense_records) == len(raw_data_offense_records)
    assert len(stored_actions) == len(raw_data_actions)
    for action in stored_actions:
        assert action in raw_data_actions


def test_ciprs_record_create_multi():
    batch = BatchFactory()
    data = record_data(1)
    CIPRSRecord.objects.create_record(batch=batch, label=batch.label, data=data)
    CIPRSRecord.objects.create_record(batch=batch, label=batch.label, data=data)
    CIPRSRecord.objects.create_record(batch=batch, label=batch.label, data=data)
    records = CIPRSRecord.objects.filter(data=data)
    for ciprs_record in records:
        assert ciprs_record.batch == batch
        assert ciprs_record.label == batch.label
        assert ciprs_record.file_no == data["General"].get("File No", "")
        assert ciprs_record.county == data["General"].get("County", "")
        assert ciprs_record.dob.strftime("%Y-%m-%d") == data["Defendant"].get(
            "Date of Birth/Estimated Age", None
        )
        assert ciprs_record.sex == data["Defendant"].get("Sex", "")
        assert ciprs_record.race == data["Defendant"].get("Race", "")
        assert ciprs_record.case_status == data["Case Information"].get(
            "Case Status", ""
        )
        record_offense_date_str = ciprs_record.offense_date.astimezone(
            pytz.timezone(settings.TIME_ZONE)
        ).strftime("%Y-%m-%dT%H:%M:%S")
        data_offense_date_str = data.get("Case Information", {}).get(
            "Offense Date", None
        )
        assert record_offense_date_str == data_offense_date_str
        data_arrest_date = data.get("Offense Record", {}).get("Arrest Date", "")
        if not data_arrest_date:
            data_arrest_date = dt_obj_to_date(ciprs_record.offense_date).strftime(
                "%Y-%m-%d"
            )
        assert ciprs_record.arrest_date.strftime("%Y-%m-%d") == data_arrest_date
        # Offense Assertions
        assert ciprs_record.offenses.first().disposed_on.strftime(
            "%Y-%m-%d"
        ) == ciprs_record.data.get("Offense Record").get("Disposed On")
        assert ciprs_record.offenses.first().disposition_method == ciprs_record.data.get(
            "Offense Record"
        ).get(
            "Disposition Method"
        )

        # OffenseRecord Assertions
        raw_data_actions = []
        raw_data_offense_records = ciprs_record.data.get("Offense Record").get(
            "Records"
        )
        for offense_record in raw_data_offense_records:
            for key, value in offense_record.items():
                if "Action" in key:
                    raw_data_actions.extend(value)
        stored_actions = []
        stored_offense_records = list(
            ciprs_record.offenses.first().offense_records.all()
        )
        for offense_record in stored_offense_records:
            stored_actions.extend(offense_record.action)

        assert len(stored_offense_records) == len(raw_data_offense_records)
        assert len(stored_actions) == len(raw_data_actions)
        for action in stored_actions:
            assert action in raw_data_actions


def test_ciprs_record_create_empty_data_dict():
    """Test the create_record method when an empty data dict is passed to it
    """
    batch = BatchFactory()
    data = {}
    CIPRSRecord.objects.create_record(batch=batch, label=batch.label, data=data)
    ciprs_record = CIPRSRecord.objects.get(data=data)
    assert ciprs_record.batch == batch
    assert ciprs_record.label == batch.label
    assert ciprs_record.file_no == ""
    assert ciprs_record.county == ""
    assert ciprs_record.dob == None
    assert ciprs_record.sex == "N/A"
    assert ciprs_record.race == ""
    assert ciprs_record.case_status == ""
    assert ciprs_record.offense_date == None
    assert ciprs_record.arrest_date == None
    offenses = ciprs_record.offenses.first()
    offense_records = list(OffenseRecord.objects.filter(offense=offenses))
    assert offenses == None
    assert offense_records == []


def test_refresh_record_from_data():
    """Test that General, Case, and Defendant Fields are generated from raw data"""
    ciprs_record = CIPRSRecordFactory()
    # Prior to calling refresh_record_from_data(), the following fields do not
    # have the values from the ciprs_record's data attribute.
    assert ciprs_record.file_no != ciprs_record.data["General"].get("File No", "")
    assert ciprs_record.county != ciprs_record.data["General"].get("County", "")
    assert ciprs_record.dob != ciprs_record.data["Defendant"].get(
        "Date of Birth/Estimated Age", None
    )
    ciprs_record.refresh_record_from_data()
    assert ciprs_record.file_no == ciprs_record.data["General"].get("File No", "")
    assert ciprs_record.county == ciprs_record.data["General"].get("County", "")
    assert ciprs_record.dob == ciprs_record.data["Defendant"].get(
        "Date of Birth/Estimated Age", None
    )
    assert ciprs_record.sex == ciprs_record.data["Defendant"].get("Sex", "")
    assert ciprs_record.race == ciprs_record.data["Defendant"].get("Race", "")
    assert ciprs_record.case_status == ciprs_record.data["Case Information"].get(
        "Case Status", ""
    )
    assert ciprs_record.offense_date.strftime(
        "%Y-%m-%dT%H:%M:%S"
    ) == make_datetime_aware(
        ciprs_record.data["Case Information"].get("Offense Date", None)
    ).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    assert ciprs_record.arrest_date == ciprs_record.data["Offense Record"].get(
        "Arrest Date", dt_obj_to_date(ciprs_record.offense_date)
    )

    # Offense Assertions
    assert ciprs_record.offenses.first().disposed_on.strftime(
        "%Y-%m-%d"
    ) == ciprs_record.data.get("Offense Record").get("Disposed On")
    assert ciprs_record.offenses.first().disposition_method == ciprs_record.data.get(
        "Offense Record"
    ).get("Disposition Method")

    # OffenseRecord Assertions
    raw_data_actions = []
    raw_data_offense_records = ciprs_record.data.get("Offense Record").get("Records")
    for offense_record in raw_data_offense_records:
        for key, value in offense_record.items():
            if "Action" in key:
                raw_data_actions.extend(value)
    stored_actions = []
    stored_offense_records = list(ciprs_record.offenses.first().offense_records.all())
    for offense_record in stored_offense_records:
        stored_actions.extend(offense_record.action)

    assert len(stored_offense_records) == len(raw_data_offense_records)
    assert len(stored_actions) == len(raw_data_actions)
    for action in stored_actions:
        assert action in raw_data_actions

    # update file_no, sex, and offense_date attributes in the raw data dictionary and refresh the record
    file_no = "ABC29304"
    sex = "M"
    offense_date = "2019-04-01T20:30:20"
    ciprs_record.data["General"]["File No"] = file_no
    ciprs_record.data["Defendant"]["Sex"] = sex
    ciprs_record.data["Case Information"]["Offense Date"] = offense_date
    ciprs_record.refresh_record_from_data()
    # assert that the file_no, sex, and offense_date field has changed on the instance
    assert ciprs_record.file_no == file_no
    assert ciprs_record.sex == sex
    assert ciprs_record.offense_date.strftime(
        "%Y-%m-%dT%H:%M:%S"
    ) == make_datetime_aware(offense_date).strftime("%Y-%m-%dT%H:%M:%S")


def test_refresh_record_from_data_empty_data_dict():
    ciprs_record = CIPRSRecordFactory()
    ciprs_record.refresh_record_from_data()
    assert ciprs_record.file_no == ciprs_record.data["General"].get("File No", "")
    assert ciprs_record.county == ciprs_record.data["General"].get("County", "")
    assert ciprs_record.dob == ciprs_record.data["Defendant"].get(
        "Date of Birth/Estimated Age", None
    )
    assert ciprs_record.sex == ciprs_record.data["Defendant"].get("Sex", "")
    assert ciprs_record.race == ciprs_record.data["Defendant"].get("Race", "")
    assert ciprs_record.case_status == ciprs_record.data["Case Information"].get(
        "Case Status", ""
    )
    assert ciprs_record.offense_date.strftime(
        "%Y-%m-%dT%H:%M:%S"
    ) == make_datetime_aware(
        ciprs_record.data["Case Information"].get("Offense Date", None)
    ).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    assert ciprs_record.arrest_date == ciprs_record.data["Offense Record"].get(
        "Arrest Date", dt_obj_to_date(ciprs_record.offense_date)
    )

    ciprs_record.data = {}
    ciprs_record.refresh_record_from_data()
    assert ciprs_record.file_no == ""
    assert ciprs_record.county == ""
    assert ciprs_record.dob == None
    assert ciprs_record.sex == "N/A"
    assert ciprs_record.race == ""
    assert ciprs_record.case_status == ""
    assert ciprs_record.offense_date == None
    assert ciprs_record.arrest_date == None
    offenses = ciprs_record.offenses.first()
    offense_records = list(OffenseRecord.objects.filter(offense=offenses))
    assert offenses == None
    assert offense_records == []


def test_refresh_record_from_data_multi():
    ciprs_record = CIPRSRecordFactory()
    file_no = "ABC29304"
    ciprs_record.refresh_record_from_data()
    ciprs_record.refresh_record_from_data()
    ciprs_record.refresh_record_from_data()
    # We shouldn't see a change in our assertion after calling refresh_record_from_data multiple times
    assert ciprs_record.file_no == ciprs_record.data["General"].get("File No", "")
    assert ciprs_record.county == ciprs_record.data["General"].get("County", "")
    assert ciprs_record.dob == ciprs_record.data["Defendant"].get(
        "Date of Birth/Estimated Age", None
    )
    assert ciprs_record.sex == ciprs_record.data["Defendant"].get("Sex", "")
    assert ciprs_record.race == ciprs_record.data["Defendant"].get("Race", "")
    assert ciprs_record.case_status == ciprs_record.data["Case Information"].get(
        "Case Status", ""
    )
    assert ciprs_record.offense_date.strftime(
        "%Y-%m-%dT%H:%M:%S"
    ) == make_datetime_aware(
        ciprs_record.data["Case Information"].get("Offense Date", None)
    ).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    assert ciprs_record.arrest_date == ciprs_record.data["Offense Record"].get(
        "Arrest Date", dt_obj_to_date(ciprs_record.offense_date)
    )
    # Offense Assertions
    assert ciprs_record.offenses.first().disposed_on.strftime(
        "%Y-%m-%d"
    ) == ciprs_record.data.get("Offense Record").get("Disposed On")
    assert ciprs_record.offenses.first().disposition_method == ciprs_record.data.get(
        "Offense Record"
    ).get("Disposition Method")

    # OffenseRecord Assertions
    raw_data_actions = []
    raw_data_offense_records = ciprs_record.data.get("Offense Record").get("Records")
    for offense_record in raw_data_offense_records:
        for key, value in offense_record.items():
            if "Action" in key:
                raw_data_actions.extend(value)
    stored_actions = []
    stored_offense_records = list(ciprs_record.offenses.first().offense_records.all())
    for offense_record in stored_offense_records:
        stored_actions.extend(offense_record.action)

    assert len(stored_offense_records) == len(raw_data_offense_records)
    assert len(stored_actions) == len(raw_data_actions)
    for action in stored_actions:
        assert action in raw_data_actions
    # update file_no attribute in the raw data dictionary and refresh the record
    ciprs_record.data["General"]["File No"] = file_no
    ciprs_record.refresh_record_from_data()
    # assert that the file_no field has changed on the instance
    assert ciprs_record.file_no == file_no
