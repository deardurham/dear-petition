import pytest
from datetime import date

from dear_petition.petition.export.documents.expungable_summary import generate_context
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory, OffenseRecordFactory, OffenseFactory,
)
from dear_petition.petition.constants import (
    DISP_METHOD_SUPERSEDING_INDICTMENT,
    DISTRICT_COURT,
    SUPERIOR_COURT,
    VERDICT_GUILTY,
    VERDICT_CODE_GUILTY,
    VERDICT_CODE_GUILTY_TO_LESSER,
    CHARGED,
    CONVICTED,
)

pytestmark = pytest.mark.django_db

PETITIONER_INFO = {
    "name": "Pete Petitioner"
}


def test_expungable_summary_context__one_table_one_row(batch, contact1):
    """
    Test generate_context method with one table and one row. Test all data
    """
    offense = create_offense(batch, "DURHAM", DISTRICT_COURT, "10CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

    assert context["attorney"] == contact1.name
    assert context["petitioner"] == PETITIONER_INFO["name"]
    assert context["dob"] == "12/31/1972"
    assert context["birthday_18th"] == "12/31/1990"
    assert context["birthday_22nd"] == "12/31/1994"

    first_table = context["tables"][0]
    assert first_table["idx"] == 1
    assert first_table["county"] == "DURHAM"
    assert first_table["jurisdiction"] == "DISTRICT COURT"

    first_offense_record = first_table["offense_records"][0]
    assert first_offense_record["file_no"] == "10CR000001"
    assert first_offense_record["arrest_date"] == "10/01/2001"
    assert first_offense_record["description"] == "SIMPLE ASSAULT"
    assert first_offense_record["severity"] == "M"
    assert first_offense_record["offense_date"] == "09/30/2001"
    assert first_offense_record["disposition"] == "NG"
    assert first_offense_record["disposed_on"] == "10/02/2003"


def test_expungable_summary_context__many_tables(batch, contact1):
    """
    Test generate_context method with many tables. Make sure correct number of tables and in correct order.
    """
    offense1 = create_offense(batch, "WAKE", SUPERIOR_COURT, "11CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense1, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense2 = create_offense(batch, "DURHAM", DISTRICT_COURT, "12CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense2, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense3 = create_offense(batch, "DURHAM", SUPERIOR_COURT, "10CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense3, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense4 = create_offense(batch, "DURHAM", DISTRICT_COURT, "12CR000002", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense4, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

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


def test_expungable_summary_context__many_offense_records(batch, contact1):
    """
    Test generate_context method with many offense records in a table. Make sure correct number of offense records and
    in correct order.
    """
    offense1 = create_offense(batch, "DURHAM", DISTRICT_COURT, "12CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense1, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense2 = create_offense(batch, "DURHAM", DISTRICT_COURT, "10CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense2, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense3 = create_offense(batch, "DURHAM", DISTRICT_COURT, "11CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense3, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense4 = create_offense(batch, "WAKE", DISTRICT_COURT, "13CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense4, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

    # offense records for Durham District Court
    offense_records = context["tables"][0]["offense_records"]

    # there should be one row for each offense record
    assert len(offense_records) == 3

    # the offense records should be in order alphabetically by file_no
    assert offense_records[0]["file_no"] == "10CR000001"
    assert offense_records[1]["file_no"] == "11CR000001"
    assert offense_records[2]["file_no"] == "12CR000001"


def test_expungable_summary_context__exclude_superseding_indictment(batch, contact1):
    """
    Test generate_context method where one offense record has an offense with a disposition "SUPERSEDING INDICTMENT OR
    PROCESS". That offense record should be excluded.
    """
    ciprs_record = CIPRSRecordFactory(
        county="DURHAM",
        jurisdiction=DISTRICT_COURT,
        file_no="10CR000001",
        dob="1972-12-31",
        batch=batch,
        offense_date="2001-09-30",
        arrest_date="2001-10-01"
    )

    offense_si = OffenseFactory(
        ciprs_record=ciprs_record,
        disposition_method=DISP_METHOD_SUPERSEDING_INDICTMENT,
        disposed_on="2003-10-02"
    )
    OffenseRecordFactory(offense=offense_si)

    offense_npc = OffenseFactory(
        ciprs_record=ciprs_record,
        disposition_method="NO PROBABLE CAUSE",
        disposed_on="2004-11-03"
    )
    OffenseRecordFactory(offense=offense_npc)

    context = generate_context(batch, contact1, PETITIONER_INFO)

    # There should be one table and one offense record
    assert len(context["tables"]) == 1
    first_table = context["tables"][0]
    assert len(first_table["offense_records"]) == 1

    # The offense record should not be the "SUPERSEDING INDICTMENT OR PROCESS" one.
    first_offense_record = first_table["offense_records"][0]
    assert first_offense_record["disposition"] == "NPC"


def test_expungable_summary_context__duplicate(batch, contact1):
    """
    Test generate_context method with identical charged and convicted offense records that are part of same offense.
    Only one of the two offense records should be included. It doesn't matter which one since they are identical except
    for the offense records' action (eg CHARGED, CONVICTED) which isn't included in the result.
    """
    offense = create_offense(batch, "DURHAM", DISTRICT_COURT, "10CR000001", "1972-12-31", VERDICT_GUILTY, "JURY TRIAL")
    create_offense_record(offense, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")
    create_offense_record(offense, CONVICTED, "SIMPLE ASSAULT", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

    # offense records for Durham District Court
    offense_records = context["tables"][0]["offense_records"]

    # there should only be one offense record
    assert len(offense_records) == 1


def test_expungable_summary_context__different_descriptions(batch, contact1):
    """
    Test generate_context method with different charged and convicted offense records (different descriptions) that are
    part of same offense. The charged offense record's disposition should be guilty to lesser and the convicted offense
    record's disposition should be guilty.
    """
    offense1 = create_offense(batch, "DURHAM", DISTRICT_COURT, "10CR000001", "1972-12-31", VERDICT_GUILTY, "JURY TRIAL")
    create_offense_record(offense1, CHARGED, "PWIMSD SCH II CS", "MISDEMEANOR")
    create_offense_record(offense1, CONVICTED, "FELONY POSSESSION OF COCAINE", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

    # offense records for Durham District Court
    offense_records = context["tables"][0]["offense_records"]

    assert len(offense_records) == 2

    # The CHARGED offense record should have a disposition method of guilty to lesser
    assert offense_records[0]["description"] == "PWIMSD SCH II CS"
    assert offense_records[0]["disposition"] == VERDICT_CODE_GUILTY_TO_LESSER

    # The CONVICTED offense record should have a disposition method of guilty
    assert offense_records[1]["description"] == "FELONY POSSESSION OF COCAINE"
    assert offense_records[1]["disposition"] == VERDICT_CODE_GUILTY


def test_expungable_summary_context__different_severities(batch, contact1):
    """
    Test generate_context method with different charged and convicted offense records (different severities) that are
    part of same offense. The charged offense record's disposition should be guilty to lesser and the convicted offense
    record's disposition should be guilty.
    """
    offense1 = create_offense(batch, "DURHAM", DISTRICT_COURT, "10CR000001", "1972-12-31", VERDICT_GUILTY, "JURY TRIAL")
    create_offense_record(offense1, CHARGED, "FLEE/ELUDE ARREST W/MV", "FELONY")
    create_offense_record(offense1, CONVICTED, "FLEE/ELUDE ARREST W/MV", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

    # offense records for Durham District Court
    offense_records = context["tables"][0]["offense_records"]

    assert len(offense_records) == 2

    # The CHARGED offense record should have a disposition method of guilty to lesser
    assert offense_records[0]["severity"] == "F"
    assert offense_records[0]["disposition"] == VERDICT_CODE_GUILTY_TO_LESSER

    # The CONVICTED offense record should have a disposition method of guilty
    assert offense_records[1]["severity"] == "M"
    assert offense_records[1]["disposition"] == VERDICT_CODE_GUILTY


def test_expungable_summary_context__disposition_codes(batch, contact1):
    """
    Test generate_context method where the disposition code comes from the disposition map, the verdict map, and isn't
    found in either map.
    """
    offense1 = create_offense(batch, "DURHAM", DISTRICT_COURT, "01CR000001", "1972-12-31", "", "JURY TRIAL")
    create_offense_record(offense1, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense2 = create_offense(batch, "DURHAM", DISTRICT_COURT, "02CR000001", "1972-12-31", "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense2, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    offense3 = create_offense(batch, "DURHAM", DISTRICT_COURT, "03CR000001", "1972-12-31", "", "not found")
    create_offense_record(offense3, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

    # offense records for Durham District Court
    offense_records = context["tables"][0]["offense_records"]

    # verify the disposition codes
    assert len(offense_records) == 3
    assert offense_records[0]["disposition"] == "JR"
    assert offense_records[1]["disposition"] == "NG"
    assert offense_records[2]["disposition"] == "not found"


@pytest.mark.parametrize("dob, formatted_dob, formatted_18th_bday, formatted_22nd_bday", [
    (date(1972, 12, 31), "12/31/1972", "12/31/1990", "12/31/1994"),
    # born in leap year
    (date(1988, 2, 29), "02/29/1988", "03/01/2006", "03/01/2010"),
])
def test_expungable_summary_context__birthdays(
    batch,
    contact1,
    dob,
    formatted_dob,
    formatted_18th_bday,
    formatted_22nd_bday
):
    """
    Test generate_context method with different dates of birth
    """
    offense = create_offense(batch, "DURHAM", DISTRICT_COURT, "10CR000001", dob, "NOT GUILTY", "JURY TRIAL")
    create_offense_record(offense, CHARGED, "SIMPLE ASSAULT", "MISDEMEANOR")

    context = generate_context(batch, contact1, PETITIONER_INFO)

    assert context["dob"] == formatted_dob
    assert context["birthday_18th"] == formatted_18th_bday
    assert context["birthday_22nd"] == formatted_22nd_bday


def create_offense_record(offense, action, description, severity):
    """
    Create offense record
    """
    offense_record = OffenseRecordFactory(
        offense=offense,
        action = action,
        description = description,
        severity = severity,
    )

    return offense_record


def create_offense(batch, county, jursidiction, file_no, dob, verdict, disposition_method):
    """
    Create offense
    """
    ciprs_record = CIPRSRecordFactory(
        batch=batch,
        county=county,
        jurisdiction=jursidiction,
        file_no=file_no,
        dob=dob,
        offense_date="2001-09-30",
        arrest_date="2001-10-01",
    )
    offense = OffenseFactory(
        ciprs_record=ciprs_record,
        verdict=verdict,
        disposition_method=disposition_method,
        disposed_on="2003-10-02",
    )

    return offense
