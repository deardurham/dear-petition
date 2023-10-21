import pathlib

from bs4 import BeautifulSoup
import pytest

from dear_petition.portal.etl.parsers import (
    case_info,
    case_summary,
    party_info,
    dispositions,
)


@pytest.fixture(scope="module")
def sample_record():
    path = pathlib.Path(__file__).parent / "data" / "record.html"
    return path.read_text()


@pytest.fixture(scope="module")
def soup(sample_record):
    return BeautifulSoup(sample_record, features="html.parser")


class TestCaseInfo:
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


class TestCaseSummary:
    def test_parse_filno(self, soup):
        assert case_summary.parse_case_number(soup) == "01CR012345-678"

    def test_parse_county(self, soup):
        assert case_summary.parse_county(soup) == "Wake"

    def test_district_court(self, soup):
        assert case_summary.parse_court(soup) == "District"


class TestDispositions:
    def test_parse_event_date(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert dispositions.parse_event_date(div) == "12/01/2001"

    def test_parse_event(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert dispositions.parse_event(div) == "Disposition"

    def test_parse_charge_number(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert dispositions.parse_charge_number(div) == "01"

    def test_parse_charge_offense(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert (
            dispositions.parse_charge_offense(div) == "EXTRADITION/FUGITIVE OTH STATE"
        )

    def test_parse_criminal_disposition(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert (
            dispositions.parse_criminal_disposition(div)
            == "District Dismissed by the Court - No Plea Agreement"
        )


class TestPartyInfo:
    def test_parse_defendant_name(self, soup):
        assert party_info.parse_defendant_name(soup) == "DOE, JANE EMMA"
