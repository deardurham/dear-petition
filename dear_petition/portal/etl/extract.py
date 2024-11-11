from bs4 import BeautifulSoup

from .models import CaseSummary, PartyInfo, PortalRecord
from .parsers import case_summary, dispositions, case_info, party_info


def extract_portal_record(source):
    """Parse HTML source to extract eCourts Portal record"""
    soup = BeautifulSoup(source, features="html.parser")
    return PortalRecord(
        case_summary=parse_case_summary(soup),
        case_info=case_info.parse_case_information(soup),
        party_info=parse_party_information(soup),
        dispositions=dispositions.parse_dispositions(soup),
    )


def parse_case_summary(soup):
    """Case Summary section"""
    return CaseSummary(
        case_number=case_summary.parse_case_number(soup) or "",
        county=case_summary.parse_county(soup) or "",
        court=case_summary.parse_court(soup) or "",
    )


def parse_party_information(soup):
    """Party Information section"""
    return PartyInfo(
        defendant_name=party_info.parse_defendant_name(soup),
        defendant_race=party_info.parse_defendant_race(soup) or "",
        defendant_sex=party_info.parse_defendant_sex(soup) or "",
    )
