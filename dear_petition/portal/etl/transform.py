import re

from .extract import extract_portal_record
from .models import PortalRecord
from ...petition import constants as pc


def transform_portal_record(source, location=""):
    """Transform eCourts Portal record to CIPRS-looking record."""
    record_id = re.search(r"#/([A-Za-z0-9]+)", location).group(1) if location else None
    portal_record = extract_portal_record(source, record_id)
    court = portal_record.case_summary.court
    sex = portal_record.party_info.defendant_sex
    return {
        "General": {
            "County": portal_record.case_summary.county,
            "File No": portal_record.case_summary.case_number,
            court: "Yes",
        },
        "Case Information": {
            "Case Status": portal_record.case_info.case_status,
            "Offense Date": portal_record.transform_offense_date(),
            "Arrest Date": portal_record.transform_arrest_date(),
        },
        "Defendant": {
            "Name": portal_record.party_info.defendant_name,
            "Race": portal_record.party_info.defendant_race,
            "Sex": pc.SEX_MAP[sex] if sex else "",
        },
        "District Court Offense Information": (
            transform_offenses(portal_record) if court == "District" else []
        ),
        "Superior Court Offense Information": (
            transform_offenses(portal_record) if court == "Superior" else []
        ),
        "_meta": {
            "portal_record": portal_record.model_dump_json(),
            "source": source,
            "location": location,
        },
    }


def transform_offenses(portal_record: PortalRecord):
    """Transform Portal dispositions to CIPRS offenses"""
    offenses = []
    for disposition in portal_record.dispositions:
        charge = portal_record.get_charge_by_number(disposition.charge_number)
        offense = {
            "Records": [
                {
                    "Law": charge.statute if charge else "",
                    "Count": disposition.charge_number,
                    "Severity": charge.transform_severity() if charge else "",
                    "Description": disposition.charge_offense,
                    "Agency": charge.agency if charge else None,
                }
            ],
            "Disposed On": portal_record.case_info.case_status_date.isoformat(),
            "Disposition Method": disposition.transform_disposition_method(),
        }
        offenses.append(offense)
    return offenses
