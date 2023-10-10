import logging
import re

from .utils import catch_parse_error


logger = logging.getLogger(__name__)

COUNTY_COURT_REGEX = re.compile(r"([\w\s]+)(District|Superior) Court")
FILENO_REGEX = re.compile(r"\d\dCR\d\d\d\d\d\d-\d\d\d")


@catch_parse_error
def parse_case_number(soup):
    div = soup.find("div", string=re.compile(r"\s?Case Number\s?"))
    match = FILENO_REGEX.search(div.parent.text)
    return match.group() if match else ""


@catch_parse_error
def parse_county(soup):
    div = soup.find("div", string=re.compile(r"\sLocation:\s"))
    full_court = div.parent.css.select_one("div.roa-value").text.strip()
    return COUNTY_COURT_REGEX.match(full_court).group(1).strip()


@catch_parse_error
def parse_court(soup):
    div = soup.find("div", string=re.compile(r"\sLocation:\s"))
    full_court = div.parent.css.select_one("div.roa-value").text.strip()
    return COUNTY_COURT_REGEX.match(full_court).group(2).strip()
