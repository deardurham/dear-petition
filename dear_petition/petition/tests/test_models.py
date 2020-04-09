import pytest

from .factories import (
    BatchFactory,
    CIPRSRecordFactory,
    record_data,
)

from ..models import CIPRSRecord

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
    assert ciprs_record.offense_date.strftime("%Y-%m-%dT%H:%M:%S") == data[
        "Case Information"
    ].get("Offense Date", None)
    assert ciprs_record.arrest_date == data["Offense Record"].get(
        "Arrest Date", dt_obj_to_date(ciprs_record.offense_date)
    )


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
        assert ciprs_record.offense_date.strftime("%Y-%m-%dT%H:%M:%S") == data[
            "Case Information"
        ].get("Offense Date", None)
        assert ciprs_record.arrest_date == data["Offense Record"].get(
            "Arrest Date", dt_obj_to_date(ciprs_record.offense_date)
        )


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
    # update file_no attribute in the raw data dictionary and refresh the record
    ciprs_record.data["General"]["File No"] = file_no
    ciprs_record.refresh_record_from_data()
    # assert that the file_no field has changed on the instance
    assert ciprs_record.file_no == file_no
