import pytest
from datetime import date

from dear_petition.petition import constants
from dear_petition.petition.export.documents.expungable_summary import generate_context
from dear_petition.petition.tests.factories import (
    AttorneyFactory, CIPRSRecordFactory, ClientFactory, OffenseRecordFactory, OffenseFactory,
)

pytestmark = pytest.mark.django_db

PETITIONER_INFO = {
    "name": "Pete Petitioner"
}


def test_expungable_summary_context__one_table_one_row(batch):
    """
    Test generate_context method with one table and one row. Test all data
    """
    create_offense_record("DURHAM", constants.DISTRICT_COURT, "10CR000001", "1972-12-31", batch)

    attorney = AttorneyFactory(name="A. Tourney")
    client = ClientFactory(**PETITIONER_INFO)
    context = generate_context(batch, attorney, client)

    assert context["attorney"] == 'A. Tourney'
    assert context["petitioner"] == PETITIONER_INFO["name"]
    assert context["dob"] == date(1972, 12, 31)
    assert context["birthday_18th"] == date(1990, 12, 31)
    assert context["birthday_22nd"] == date(1994, 12, 31)

    first_table = context["tables"][0]
    assert first_table["idx"] == 1
    assert first_table["county"] == "DURHAM"
    assert first_table["jurisdiction"] == "DISTRICT COURT"

    first_offense_record = first_table["offense_records"][0]
    assert first_offense_record["file_no"] == "10CR000001"
    assert first_offense_record["arrest_date"] == date(2001, 10, 1)
    assert first_offense_record["description"] == "SPEEDING(96 mph in a 70 mph zone) "
    assert first_offense_record["severity"] == "T"
    assert first_offense_record["offense_date"] == "2001-09-30"
    assert first_offense_record["disposition_method"] == "NPC"
    assert first_offense_record["disposed_on"] == date(2003, 10, 2)


def test_expungable_summary_context__many_tables(batch):
    """
    Test generate_context method with many tables. Make sure correct number of tables and in correct order.
    """
    create_offense_record("WAKE", constants.SUPERIOR_COURT, "11CR000001", "1972-12-31", batch)
    create_offense_record("DURHAM", constants.DISTRICT_COURT, "12CR000001", "1972-12-31", batch)
    create_offense_record("DURHAM", constants.SUPERIOR_COURT, "10CR000001", "1972-12-31", batch)
    create_offense_record("DURHAM", constants.DISTRICT_COURT, "12CR000002", "1972-12-31", batch)

    attorney = AttorneyFactory(name="B. Tourney")
    client = ClientFactory(**PETITIONER_INFO)
    context = generate_context(batch, attorney, client)

    # there should be one table per unique county, jurisdiction

    assert len(context["tables"]) == 3

    # the tables should be in order alphabetically by county, then district

    first_table = context["tables"][0]
    assert first_table["idx"] == 1
    assert first_table["county"] == "DURHAM"
    assert first_table["jurisdiction"] == "DISTRICT COURT"

    second_table = context["tables"][1]
    assert second_table["idx"] == 2
    assert second_table["county"] == "DURHAM"
    assert second_table["jurisdiction"] == "SUPERIOR COURT"

    third_table = context["tables"][2]
    assert third_table["idx"] == 3
    assert third_table["county"] == "WAKE"
    assert third_table["jurisdiction"] == "SUPERIOR COURT"


def test_expungable_summary_context__many_offense_records(batch):
    """
    Test generate_context method with many offense records in a table. Make sure correct number of offense records and
    in correct order.
    """
    create_offense_record("DURHAM", constants.DISTRICT_COURT, "12CR000001", "1972-12-31", batch)
    create_offense_record("DURHAM", constants.DISTRICT_COURT, "10CR000001", "1972-12-31", batch)
    create_offense_record("DURHAM", constants.DISTRICT_COURT, "11CR000001", "1972-12-31", batch)
    create_offense_record("WAKE", constants.DISTRICT_COURT, "13CR000001", "1972-12-31", batch)

    attorney = AttorneyFactory(name="C. Tourney")
    client = ClientFactory(**PETITIONER_INFO)
    context = generate_context(batch, attorney, client)

    # offense records for Durham District Court
    offense_records = context["tables"][0]["offense_records"]

    # there should be one row for each offense record
    assert len(offense_records) == 3

    # the offense records should be in order alphabetically by file_no
    assert offense_records[0]["file_no"] == "10CR000001"
    assert offense_records[1]["file_no"] == "11CR000001"
    assert offense_records[2]["file_no"] == "12CR000001"


def test_expungable_summary_context__exclude_superseding_indictment(batch):
    """
    Test generate_context method where one offense record has an offense with a disposition "SUPERSEDING INDICTMENT OR
    PROCESS". That offense record should be excluded.
    """
    ciprs_record = CIPRSRecordFactory(
        county="DURHAM",
        jurisdiction=constants.DISTRICT_COURT,
        file_no="10CR000001",
        dob="1972-12-31",
        batch=batch,
        offense_date="2001-09-30",
        arrest_date="2001-10-01"
    )

    offense_si = OffenseFactory(
        ciprs_record=ciprs_record,
        disposition_method=constants.SUPERSEDING_INDICTMENT_OR_PROCESS,
        disposed_on="2003-10-02"
    )
    OffenseRecordFactory(offense=offense_si)

    offense_npc = OffenseFactory(
        ciprs_record=ciprs_record,
        disposition_method="NO PROBABLE CAUSE",
        disposed_on="2004-11-03"
    )
    OffenseRecordFactory(offense=offense_npc)

    attorney = AttorneyFactory(name="D. Tourney")
    client = ClientFactory(**PETITIONER_INFO)
    context = generate_context(batch, attorney, client)

    # There should be one table and one offense record
    assert len(context["tables"]) == 1
    first_table = context["tables"][0]
    assert len(first_table["offense_records"]) == 1

    # The offense record should not be the "SUPERSEDING INDICTMENT OR PROCESS" one.
    first_offense_record = first_table["offense_records"][0]
    assert first_offense_record["disposition_method"] == "NPC"


@pytest.mark.parametrize("input_dob, input_18th_bday, input_22nd_bday", [
    (date(1972, 12, 31), date(1990, 12, 31), date(1994, 12, 31)),
    # born in leap year
    (date(1988, 2, 29), date(2006, 3, 1), date(2010, 3, 1)),
])
def test_expungable_summary_context__birthdays(batch, input_dob, input_18th_bday, input_22nd_bday):
    """
    Test generate_context method with different dates of birth
    """
    create_offense_record("DURHAM", constants.DISTRICT_COURT, "10CR000001", input_dob, batch)

    attorney = AttorneyFactory(name="E. Tourney")
    client = ClientFactory(**PETITIONER_INFO)
    context = generate_context(batch, attorney, client)

    assert context["dob"] == input_dob
    assert context["birthday_18th"] == input_18th_bday
    assert context["birthday_22nd"] == input_22nd_bday


def create_offense_record(county, jursidiction, file_no, dob, batch):
    """
    Create offense record
    """
    ciprs_record = CIPRSRecordFactory(
        county=county,
        jurisdiction=jursidiction,
        file_no=file_no,
        dob=dob,
        batch=batch,
        offense_date="2001-09-30",
        arrest_date="2001-10-01"
    )
    offense = OffenseFactory(
        ciprs_record=ciprs_record,
        disposition_method="NO PROBABLE CAUSE",
        disposed_on="2003-10-02"
    )
    OffenseRecordFactory(
        offense=offense
    )
