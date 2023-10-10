from functools import wraps
import logging
import re

from bs4 import BeautifulSoup

from .models import CaseInfo, Charge

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

logger = logging.getLogger(__name__)

COUNTY_COURT_REGEX = re.compile(r"([\w\s]+)(District|Superior) Court")
FILENO_REGEX = re.compile(r"\d\dCR\d\d\d\d\d\d-\d\d\d")


def catch_parse_error(func):
    """Decorator to catch parsing errors so parsing may continue"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception(f"Exception occurred in {func}")

    return wrapper


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


# Case Information #


def parse_case_information(soup):
    # Only select tr.hide-sm rows since HTML includes two versions of the same
    # offenses (one for phone, one for large screens).
    trs = soup.select("div[ng-if*=ShowOffenses] tr.hide-sm")
    charges = []
    for tr in trs:
        charge = Charge()
        parse_statute(tr=tr, charge=charge)
        parse_charge_number(tr=tr, charge=charge)
        parse_charge_offense(tr=tr, charge=charge)
        parse_charge_degree(tr=tr, charge=charge)
        parse_charge_offense_date(tr=tr, charge=charge)
        parse_charge_filed_date(tr=tr, charge=charge)
        charges.append(charge)
    ci = CaseInfo(
        charges=charges,
        case_type=parse_case_type(soup) or "",
        case_status=parse_case_status(soup) or None,
        case_status_date=parse_case_status_date(soup) or None,
    )
    return ci


@catch_parse_error
def parse_case_type(soup):
    """
    Parse charge number (first column from row)

    Sample HTML:
        <tr class="ng-scope" ng-if="::roaSection.caseInfo.CaseType.Description" style="">
            <td class="roa-label">Case Type:</td>
            <td class="roa-value ng-binding">Criminal</td>
    """
    return soup.select_one(
        "tr[ng-if*=CaseType\\.Description] td.roa-value"
    ).text.strip()


@catch_parse_error
def parse_case_status_date(soup):
    """
    Parse case status date

    Sample HTML:
        <tr ng-if="::roaSection.caseInfo.CaseStatuses.length" class="ng-scope">
            <td class="roa-value">
                <div ng-repeat="status in ::roaSection.caseInfo.CaseStatuses" class="ng-scope">
                    <div ng-class="{'roa-text-bold':$first}" class="roa-text-bold">
                        <span class="ng-binding">05/11/2007</span>
                        <span>&nbsp;</span>
                        <span class="ng-binding">Disposed</span>
    """
    # date is always first, so just use select_one
    return soup.select_one("tr[ng-if*=caseInfo\\.CaseStatuses] span").text.strip()


@catch_parse_error
def parse_case_status(soup):
    """
    Parse case status

    Sample HTML:
        <tr ng-if="::roaSection.caseInfo.CaseStatuses.length" class="ng-scope">
            <td class="roa-value">
                <div ng-repeat="status in ::roaSection.caseInfo.CaseStatuses" class="ng-scope">
                    <div ng-class="{'roa-text-bold':$first}" class="roa-text-bold">
                        <span class="ng-binding">05/11/2007</span>
                        <span>&nbsp;</span>
                        <span class="ng-binding">Disposed</span>
    """
    # date is always first, so just use select_one
    return soup.select("tr[ng-if*=caseInfo\\.CaseStatuses] span")[-1].text.strip()


@catch_parse_error
def parse_charge_number(tr, charge):
    """
    Parse charge number (first column from row)

    Sample HTML:
        <tr hide-xs="" hide-sm="" class="hide-sm hide-xs ng-scope">
            <td class="roa-text-right">
                <span ng-if="::charge.CurrChargeNum" class="ng-binding ng-scope">
                    &nbsp;01.
                </span>
            </td>
    """
    num_text = tr.select_one("span[ng-if*=CurrChargeNum]").text.strip()
    charge.number = re.findall(r"\d+", num_text)[0]


@catch_parse_error
def parse_charge_offense(tr, charge):
    """
    Parse charge offense

    Sample HTML:
        <tr hide-xs="" hide-sm="" class="hide-sm hide-xs ng-scope">
            <td>
                <div>
                    <span class="ng-binding">EXTRADITION/FUGITIVE OTH STATE</span>
                </div>
            </td>
    """
    span = tr.select_one("td div span")
    charge.offense = span.text


def parse_statute(tr, charge):
    """
    Parse charge statute

    Sample HTML:
        <tr hide-xs="" hide-sm="" class="hide-sm hide-xs ng-scope">
            <td>
                <roa-charge-data-column ng-if="::roaSection.chargeInfo.ShowStatutes &amp;&amp; charge.ChargeOffense.Statute" label="Statute" data-value="15A-727;733;734" class="ng-scope">
                    <div class="roa-inline">
                        <div class="roa-text-bold hide-gt-sm ng-binding" hide-gt-sm="">
                            Statute
                        </div>
                        <div class="ng-binding">
                            15A-727;733;734
                        </div>
                    </div>
                </roa-charge-data-column>
            </td>
    """  # noqa
    elem = tr.select_one("roa-charge-data-column[ng-if*=ChargeOffense\\.Statute]")
    charge.statute = elem["data-value"]


@catch_parse_error
def parse_charge_degree(tr, charge):
    """
    Parse charge degree

    Sample HTML:
        <tr hide-xs="" hide-sm="" class="hide-sm hide-xs ng-scope">
            <roa-charge-data-column ng-if="::charge.ChargeOffense.Degree" label="Degree" data-value="FNC" class="ng-scope">
                <div class="roa-inline">
                    <div class="roa-text-bold hide-gt-sm ng-binding" hide-gt-sm="">
                        Degree
                    </div>
                    <div class="ng-binding">FNC</div>
                </div>
            </roa-charge-data-column>
    """  # noqa
    elem = tr.select_one("roa-charge-data-column[ng-if*=Degree]")
    charge.degree = elem["data-value"]


@catch_parse_error
def parse_charge_offense_date(tr, charge):
    """
    Parse charge degree

    Sample HTML:
        <tr hide-xs="" hide-sm="" class="hide-sm hide-xs ng-scope">
            <roa-charge-data-column ng-if="::charge.ChargeOffense.Degree" label="Degree" data-value="FNC" class="ng-scope">
                <div class="roa-inline">
                    <div class="roa-text-bold hide-gt-sm ng-binding" hide-gt-sm="">
                        Degree
                    </div>
                    <div class="ng-binding">FNC</div>
                </div>
            </roa-charge-data-column>
    """  # noqa
    elem = tr.select_one("roa-charge-data-column[ng-if*=OffenseDate]")
    charge.offense_date = elem["data-value"]


@catch_parse_error
def parse_charge_filed_date(tr, charge):
    """
    Parse charge filed date

    Sample HTML:
        <tr hide-xs="" hide-sm="" class="hide-sm hide-xs ng-scope">
            <td>
                <roa-charge-data-column ng-if="::charge.FiledDate" label="Filed Date" data-value="01/09/2001" class="ng-scope">
                    <div class="roa-inline">
                        <div class="roa-text-bold hide-gt-sm ng-binding" hide-gt-sm="">
                                Filed Date
                        </div>
                        <div class="ng-binding">01/09/2001</div>
                    </div>
                </roa-charge-data-column>
            </td>
    """  # noqa
    elem = tr.select_one("roa-charge-data-column[ng-if*=FiledDate]")
    charge.filed_date = elem["data-value"]
