import logging

from bs4 import BeautifulSoup

from .models import CaseSummary, CaseInfo, Charge, PartyInfo, PortalRecord
from .parsers import case_summary, case_info, party_info

logger = logging.getLogger(__name__)


def parse_portal_document(source):
    soup = BeautifulSoup(source, features="html.parser")
    return PortalRecord(
        case_summary=parse_case_summary(soup),
        case_info=parse_case_information(soup),
        party_info=parse_party_information(soup),
    )


def parse_case_summary(soup):
    """
    Case Summary section
    """
    return CaseSummary(
        case_number=case_summary.parse_fileno(soup),
        county=case_summary.parse_county(soup),
        court=case_summary.parse_district_court(soup),
    )


def parse_case_information(soup):
    """
    Case Information section
    """
    # Only select tr.hide-sm rows since HTML includes two versions of the same
    # offenses (one for phone, one for large screens).
    trs = soup.select("div[ng-if*=ShowOffenses] tr.hide-sm")
    charges = []
    for tr in trs:
        charges.append(
            Charge(
                statute=case_info.parse_statute(tr=tr) or "",
                number=case_info.parse_charge_number(tr=tr) or None,
                offense=case_info.parse_charge_offense(tr=tr) or "",
                degree=case_info.parse_charge_degree(tr=tr) or "",
                offense_date=case_info.parse_charge_offense_date(tr=tr) or None,
                filed_date=case_info.parse_charge_filed_date(tr=tr) or None,
            )
        )
    ci = CaseInfo(
        charges=charges,
        case_type=case_info.parse_case_type(soup) or "",
        case_status=case_info.parse_case_status(soup) or None,
        case_status_date=case_info.parse_case_status_date(soup) or None,
    )
    return ci


def parse_party_information(soup):
    """
    Party Information section
    """
    return PartyInfo(defendant_name=party_info.parse_defendant_name(soup))
