import re

from .utils import catch_parse_error


@catch_parse_error
def parse_case_type(soup):
    """
    Parse case type

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
                        <span class="ng-binding">01/02/2003</span>
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
                        <span class="ng-binding">01/02/2003</span>
                        <span>&nbsp;</span>
                        <span class="ng-binding">Disposed</span>
    """
    # date is always first, so just use select_one
    return soup.select("tr[ng-if*=caseInfo\\.CaseStatuses] span")[-1].text.strip()


@catch_parse_error
def parse_charge_number(tr):
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
    return re.findall(r"\d+", num_text)[0]


@catch_parse_error
def parse_charge_offense(tr):
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
    return span.text


def parse_statute(tr):
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
                            15A-727
                        </div>
                    </div>
                </roa-charge-data-column>
            </td>
    """  # noqa
    elem = tr.select_one("roa-charge-data-column[ng-if*=ChargeOffense\\.Statute]")
    return elem["data-value"]


@catch_parse_error
def parse_charge_degree(tr):
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
    return elem["data-value"]


@catch_parse_error
def parse_charge_offense_date(tr):
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
    return elem["data-value"]


@catch_parse_error
def parse_charge_filed_date(tr):
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
    return elem["data-value"]
