import re

from bs4 import BeautifulSoup

# From Jessica:
# 1. File numbers have changed: Instead of 05CRS****** we have 05CR****-910.
#    There is a suffix for the county code
# 2. To distinguish Superior Court vs. District Court, you look to “Location”
#    rather than “CR” vs. “CRS.”
# 3. CIPRS had summary and detail reports. Portal has one document. The
#    arresting agency is always listed.
# 4. The records no longer list a date of birth. Searches do not display date of
#    birth, but “XX/XX/XXXX” instead.
# 5. There is currently no way in Portal to download more than 1 record at a
#    time. In CIPRS, we could select multiple records into a cart and email
#    records 10 at a time.

COUNTY_COURT_REGEX = re.compile("([\w\s]+)(District|Superior) Court")
FILENO_REGEX = re.compile(r"\d\dCR\d\d\d\d\d\d-\d\d\d")


def parse_portal_document(source):
    soup = BeautifulSoup(source, features="html.parser")
    return {
        "General": {
            "County": parse_county(soup),
            "File No": parse_fileno(soup),
            "District": parse_district_court(soup),
        },
        "Defendant": {"Name": parse_defendant_name(soup)},
    }


def parse_defendant_name(soup):
    div = soup.find("div", string=re.compile(r"\s?Defendant\s?"))
    row = div.find_parent("tr")
    name = row.css.select_one("table.roa-table").text.strip()
    return name


def parse_fileno(soup):
    div = soup.find("div", string=re.compile(r"\s?Case Number\s?"))
    match = FILENO_REGEX.search(div.parent.text)
    return match.group() if match else ""


def parse_county(soup):
    div = soup.find("div", string=re.compile(r"\sLocation:\s"))
    full_court = div.parent.css.select_one("div.roa-value").text.strip()
    return COUNTY_COURT_REGEX.match(full_court).group(1).strip()


def parse_district_court(soup):
    div = soup.find("div", string=re.compile(r"\sLocation:\s"))
    full_court = div.parent.css.select_one("div.roa-value").text.strip()
    court = COUNTY_COURT_REGEX.match(full_court).group(2).strip()
    return "Yes" if court == "District" else "No"
