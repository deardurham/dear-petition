import pathlib

from bs4 import BeautifulSoup
import pytest

from dear_petition.portal.etl.parsers import case_summary, party_info


@pytest.fixture
def sample_record():
    path = pathlib.Path(__file__).parent / "data" / "record.html"
    return path.read_text()


@pytest.fixture
def soup(sample_record):
    return BeautifulSoup(sample_record, features="html.parser")


def test_parse_defendant_name(soup):
    assert party_info.parse_defendant_name(soup) == "DOE, JANE EMMA"


def test_parse_filno(soup):
    assert case_summary.parse_case_number(soup) == "01CR012345-678"


def test_parse_county(soup):
    assert case_summary.parse_county(soup) == "Wake"


def test_district_court(soup):
    assert case_summary.parse_court(soup) == "District"
