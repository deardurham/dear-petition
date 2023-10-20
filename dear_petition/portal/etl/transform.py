from .extract import extract_portal_record
from .models import PortalRecord


def transform_portal_record(source):
    """Transform eCourts Portal record to CIPRS-looking record."""
    portal_record = extract_portal_record(source)
    court = portal_record.case_summary.court
    return {
        "General": {
            "County": portal_record.case_summary.county,
            "File No": portal_record.case_summary.case_number,
            "District": "Yes" if court == "District" else "No",
        },
        "Defendant": {"Name": portal_record.party_info.defendant_name},
        "District Court Offense Information": (
            transform_offenses(portal_record) if court == "District" else []
        ),
        "Superior Court Offense Information": (
            transform_offenses(portal_record) if court == "Superior" else []
        ),
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
                    "Action": disposition.event,
                    "Severity": charge.severity,
                    "Description": disposition.charge_offense,
                }
            ],
            "Disposed On": portal_record.case_info.case_status_date.isoformat(),
            "Disposition Method": disposition.criminal_disposition,
        }
        offenses.append(offense)
    return offenses
