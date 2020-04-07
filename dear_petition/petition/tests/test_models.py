import pytest

from .factories import BatchFactory, record_data

from ..models import CIPRSRecord

from ..utils import dt_obj_to_date

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
    assert ciprs_record.file_no == data["General"].get("File No", "")
    assert ciprs_record.county == data["General"].get("County", "")
    assert ciprs_record.dob.strftime("%Y-%m-%d") == data["Defendant"].get(
        "Date of Birth/Estimated Age", ""
    )
    assert ciprs_record.sex == data["Defendant"].get("Sex", "")
    assert ciprs_record.race == data["Defendant"].get("Race", "")
    assert ciprs_record.case_status == data["Case Information"].get("Case Status", "")
    assert ciprs_record.offense_date.strftime("%Y-%m-%dT%H:%M:%S") == data[
        "Case Information"
    ].get("Offense Date", "")
    assert ciprs_record.arrest_date == data["Offense Record"].get(
        "Arrest Date", dt_obj_to_date(ciprs_record.offense_date)
    )

    def test_refresh_record_from_data():
        """Test that General, Case, and Defendant Fields are generated from raw data"""
        ciprs_record = CIPRSRecordFactory()
        ciprs_record.refresh_record_from_data()
        assert ciprs_record.file_no == ciprs_record.data["General"].get("File No", "")
        assert ciprs_record.county == ciprs_record.data["General"].get("County", "")
        assert ciprs_record.dob.strftime("%Y-%m-%d") == ciprs_record.data[
            "Defendant"
        ].get("Date of Birth/Estimated Age", "")
        assert ciprs_record.sex == ciprs_record.data["Defendant"].get("Sex", "")
        assert ciprs_record.race == ciprs_record.data["Defendant"].get("Race", "")
        assert ciprs_record.case_status == ciprs_record.data["Case Information"].get(
            "Case Status", ""
        )
        assert ciprs_record.offense_date.strftime(
            "%Y-%m-%dT%H:%M:%S"
        ) == ciprs_record.data["Case Information"].get("Offense Date", "")
        assert ciprs_record.arrest_date == ciprs_record.data["Offense Record"].get(
            "Arrest Date", dt_obj_to_date(ciprs_record.offense_date)
        )
