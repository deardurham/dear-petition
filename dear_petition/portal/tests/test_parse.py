import pathlib

from bs4 import BeautifulSoup
import pytest

from dear_petition.portal import parse


@pytest.fixture
def sample_record():
    path = pathlib.Path(__file__).parent / "data" / "record.html"
    return path.read_text()


@pytest.fixture
def soup(sample_record):
    return BeautifulSoup(sample_record, features="html.parser")


def test_parse_defendant_name(soup):
    assert parse.parse_defendant_name(soup) == "DOE, JANE EMMA"


def test_parse_filno(soup):
    assert parse.parse_fileno(soup) == "01CR012345-678"


def test_parse_county(soup):
    assert parse.parse_county(soup) == "Wake"


def test_district_court(soup):
    assert parse.parse_district_court(soup) == "Yes"
