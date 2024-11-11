import pytest

from bs4 import BeautifulSoup

from dear_petition.portal.etl.parsers import (
    case_info,
)


class TestCaseInfoFullRecord:
    def test_parse_case_type(self, soup):
        assert case_info.parse_case_type(soup) == "Criminal"

    def test_parse_case_status_date(self, soup):
        assert case_info.parse_case_status_date(soup) == "12/01/2001"

    def test_parse_case_status(self, soup):
        assert case_info.parse_case_status(soup) == "Disposed"

    def test_parse_charge_number(self, soup):
        tr = soup.select_one("div[ng-if*=ShowOffenses] tr.hide-sm")
        assert case_info.parse_charge_number(tr) == "01"

    def test_parse_charge_offense(self, soup):
        tr = soup.select_one(case_info.SELECT_OFFENSES)
        assert case_info.parse_charge_offense(tr) == "EXTRADITION/FUGITIVE OTH STATE"

    def test_parse_statute(self, soup):
        tr = soup.select_one(case_info.SELECT_OFFENSES)
        assert case_info.parse_statute(tr) == "15A-727;733;734"

    def test_parse_charge_degree(self, soup):
        tr = soup.select_one(case_info.SELECT_OFFENSES)
        assert case_info.parse_charge_degree(tr) == "FNC"

    def test_parse_charge_offense_date(self, soup):
        tr = soup.select_one(case_info.SELECT_OFFENSES)
        assert case_info.parse_charge_offense_date(tr) == "01/01/2001"

    def test_parse_charge_file_date(self, soup):
        tr = soup.select_one(case_info.SELECT_OFFENSES)
        assert case_info.parse_charge_filed_date(tr) == "01/09/2001"

    def test_parse_charge_agency(self, soup):
        tr = soup.select_one(case_info.SELECT_OFFENSES)
        agency_tr = tr.findNext("tr")
        assert agency_tr is not None
        assert case_info.parse_charge_agency(agency_tr) == "Creedmoor Police Department"


@pytest.mark.parametrize(
    "parser",
    [
        case_info.parse_case_type,
        case_info.parse_case_status_date,
        case_info.parse_case_status,
        case_info.parse_charge_number,
        case_info.parse_charge_offense,
        case_info.parse_statute,
        case_info.parse_charge_degree,
        case_info.parse_charge_offense_date,
        case_info.parse_charge_filed_date,
        case_info.parse_charge_agency,
    ],
)
def test_catch_parse_error(caplog, parser):
    """Ensure HTML parse exceptions are captured and logged"""
    soup = BeautifulSoup("<div></div>", features="html.parser")
    parser(soup)
    assert str(parser.__name__) in caplog.text
