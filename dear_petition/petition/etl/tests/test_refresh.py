import pytest

from dear_petition.petition.utils import make_datetime_aware

pytestmark = pytest.mark.django_db


def test_general_file_no(record1):
    record1.data = {"General": {"File No": "20CR012345"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.file_no == record1.data["General"]["File No"]


def test_general_county(record1):
    record1.data = {"General": {"County": "DURHAM"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.county == record1.data["General"]["County"]


def test_defendant_dob(record1):
    record1.data = {"Defendant": {"Date of Birth/Estimated Age": "2000-01-01"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert (
        record1.dob.strftime("%Y-%m-%d") == record1.data["Defendant"]["Date of Birth/Estimated Age"]
    )


def test_defendant_sex(record1):
    record1.data = {"Defendant": {"Sex": "M"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.sex == record1.data["Defendant"]["Sex"]


def test_defendant_race(record1):
    record1.data = {"Defendant": {"Race": "WHITE"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.race == record1.data["Defendant"]["Race"]


def test_case_information_case_status(record1):
    record1.data = {"Case Information": {"Case Status": "DISPOSED"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.case_status == record1.data["Case Information"]["Case Status"]


def test_case_information_offense_date(record1):
    record1.data = {"Case Information": {"Offense Date": "2000-01-01T00:00:00"}}
    expected = make_datetime_aware(record1.data["Case Information"]["Offense Date"])
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.offense_date == expected


def test_case_information_arrest_date(record1):
    record1.data = {"Case Information": {"Arrest Date": "2000-01-01"}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert (
        record1.arrest_date.strftime("%Y-%m-%d") == record1.data["Case Information"]["Arrest Date"]
    )


def test_refresh_record_from_data___has_additional_offenses_true(record1):
    """
    Since the text "Additional offenses exist" is present, has_additional_offenses should be true.
    """
    record1.data = {"_meta": {"source": "Lorem ipsum. Additional offenses exist. Lorem ipsum."}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert record1.has_additional_offenses


def test_refresh_record_from_data___has_additional_offenses_false(record1):
    """
    Since the text "Additional offenses exist" is not present, has_additional_offenses should be false.
    """
    record1.data = {"_meta": {"source": "Lorem ipsum."}}
    record1.refresh_record_from_data()
    record1.refresh_from_db()
    assert not record1.has_additional_offenses


def test_refresh_record_from_data__exclude_file_numbers_contains(record1):
    """
    CIPRS record file number is in the list of excluded file numbers.
    """
    exclude_file_nos = ["20CR000001", "20CR012345", "20CR000002"]
    record1.data = {"General": {"File No": "20CR012345"}}
    record1.refresh_record_from_data(exclude_file_nos)
    record1.refresh_from_db()
    assert record1.file_no != "20CR012345"


def test_refresh_record_from_data__exclude_file_numbers_does_not_contain(record1):
    """
    CIPRS record file number is not in the list of excluded file numbers.
    """
    exclude_file_nos = ["20CR000001"]
    record1.data = {"General": {"File No": "20CR012345"}}
    record1.refresh_record_from_data(exclude_file_nos)
    record1.refresh_from_db()
    assert record1.file_no == "20CR012345"


def test_refresh_record_from_data__exclude_file_numbers_empty(record1):
    """
    List of excluded file numbers is empty.
    """
    exclude_file_nos = []
    record1.data = {"General": {"File No": "20CR012345"}}
    record1.refresh_record_from_data(exclude_file_nos)
    record1.refresh_from_db()
    assert record1.file_no == "20CR012345"


def test_refresh_record_from_data__exclude_file_numbers_none(record1):
    """
    List of excluded file numbers is None.
    """
    exclude_file_nos = None
    record1.data = {"General": {"File No": "20CR012345"}}
    record1.refresh_record_from_data(exclude_file_nos)
    record1.refresh_from_db()
    assert record1.file_no == "20CR012345"
