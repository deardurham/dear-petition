import datetime as dt
from unittest.mock import patch

from dear_petition.portal.etl.extract import extract_portal_record
from dear_petition.portal.etl.models import (
    PortalRecord,
    CaseInfo,
    CaseSummary,
    Charge,
    PartyInfo,
    Disposition,
)


@patch("dear_petition.portal.etl.parsers.dispositions.requests")
def test_extract(mock_requests, sample_record, dispositions):
    mock_requests.get.return_value.json.return_value = dispositions
    expected = PortalRecord(
        case_summary=CaseSummary(case_number="01CR012345-678", county="Wake", court="District"),
        case_info=CaseInfo(
            case_type="Criminal",
            case_status="Disposed",
            case_status_date=dt.date(2001, 12, 1),
            charges=[
                Charge(
                    number=1,
                    offense="EXTRADITION/FUGITIVE OTH STATE",
                    statute="15A-727;733;734",
                    degree="FNC",
                    offense_date=dt.date(2001, 1, 1),
                    filed_date=dt.date(2001, 1, 9),
                    arrest_date=dt.date(2001, 1, 3),
                    agency="Creedmoor Police Department",
                )
            ],
        ),
        party_info=PartyInfo(
            defendant_name="DOE, JANE EMMA", defendant_race="White", defendant_sex="Female"
        ),
        dispositions=[
            Disposition(
                event_date=dt.date(2001, 12, 1),
                event="Disposition",
                charge_number=1,
                charge_offense="EXTRADITION/FUGITIVE OTH STATE",
                criminal_disposition="District Dismissed by the Court - No Plea Agreement",
            )
        ],
    )

    assert extract_portal_record(sample_record, record_id=123) == expected
