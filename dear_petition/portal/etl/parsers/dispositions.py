import requests
from datetime import datetime

from dear_petition.portal.etl.models import Disposition

from .utils import catch_parse_error


SELECT_DISPOSITIONS = "div[ng-if*=data\\.roaSections\\.dispositionEvents] div.roa-event-info-criminal-disposition-event"


def parse_dispositions(record_id):
    """Case Information section"""
    disposition_request = requests.get(
        f"https://portal-nc.tylertech.cloud/app/RegisterOfActionsService/DispositionEvents('{record_id}')?mode=portalembed&$top=50&$skip=0"
    )
    disposition_request.raise_for_status()
    disposition_data = disposition_request.json()
    dispositions = []
    for event in disposition_data["Events"]:
        if event["Type"] != "CriminalDispositionEvent":
            continue
        event = event["Event"]
        date = event["Date"]
        criminal_dispositions = event["CriminalDispositions"]
        for criminal_disposition in criminal_dispositions:
            criminal_disposition_type = criminal_disposition["CriminalDispositionTypeId"]
            charge = criminal_disposition["Charge"]
            charge_offense = charge["ChargeOffense"]
            dispositions.append(
                Disposition(
                    event_date=datetime.strptime(date, "%m/%d/%Y").date(),
                    charge_number=charge_offense["ChargeNumber"],
                    charge_offense=charge_offense["ChargeOffenseDescription"],
                    criminal_disposition=criminal_disposition_type["Description"],
                )
            )

    return dispositions


def parse_dispositions_by_html(soup):
    """Case Information section"""
    divs = soup.select(SELECT_DISPOSITIONS)
    dispositions = []
    for div in divs:
        dispositions.append(
            Disposition(
                event_date=parse_event_date(div),
                event=parse_event(div),
                charge_number=parse_charge_number(div),
                charge_offense=parse_charge_offense(div),
                criminal_disposition=parse_criminal_disposition(div),
            )
        )
    return dispositions


@catch_parse_error
def parse_event_date(div):
    """
    Parse disposition event date

    Sample HTML:
        <div class="roa-pad-0 roa-event-info ng-scope roa-event-info-criminal-disposition-event">
            <div class="roa-event-date-col ng-scope" ng-if="::!minuteEvent" ng-class="::$scope.checkEventDiffPriorsClass(event, 0)">
                <div ng-transclude="" ng-class="::{'roa-text-strike': event.Event.IsDeleted}">
                    <span class="ng-binding ng-scope"> 01/04/2006 </span>
                </div>
            </div>
    """  # noqa
    return div.select_one("div.roa-event-date-col").text.strip()


@catch_parse_error
def parse_event(div):
    """
    Parse disposition event date

    Sample HTML:
        <div class="roa-pad-0 roa-event-info ng-scope roa-event-info-criminal-disposition-event">
            <div class="roa-event-content">
                <div ng-class="::$scope.checkEventDiffPriorsClass(event, 0)">
                    <span class="roa-text-bold ng-binding">
                        Plea
                    </span>
                </div>
            </div>
    """
    return div.select_one("div.roa-event-content span.roa-text-bold").text.strip()


@catch_parse_error
def parse_charge_number(div):
    """
    Parse charge number

    Sample HTML:
        <div class="roa-pad-0 roa-event-info ng-scope roa-event-info-criminal-disposition-event">
            <div ng-repeat="criminalDisposition in ::event.Event.CriminalDispositions" ng-if="::event.Event.CriminalDispositions.length &amp;&amp; !criminalDisposition.Charge.HideCharge" class="ng-scope">
                <div ng-if="::criminalDisposition.Charge.ChargeOffense.ChargeNumber &amp;&amp; criminalDisposition.Charge.ChargeOffense.ChargeOffenseDescription" class="roa-indent ng-scope">
                    <div class="roa-outdent-first-line ng-binding">
                        52. MISDEMEANOR LARCENY
                    </div>
    """  # noqa
    charge = div.select_one("div[ng-if*=ChargeOffense] div").text.strip()
    return charge.split(".", maxsplit=1)[0].strip()


@catch_parse_error
def parse_charge_offense(div):
    """
    Parse charge offense

    Sample HTML:
        <div class="roa-pad-0 roa-event-info ng-scope roa-event-info-criminal-disposition-event">
            <div ng-repeat="criminalDisposition in ::event.Event.CriminalDispositions" ng-if="::event.Event.CriminalDispositions.length &amp;&amp; !criminalDisposition.Charge.HideCharge" class="ng-scope">
                <div ng-if="::criminalDisposition.Charge.ChargeOffense.ChargeNumber &amp;&amp; criminalDisposition.Charge.ChargeOffense.ChargeOffenseDescription" class="roa-indent ng-scope">
                    <div class="roa-outdent-first-line ng-binding">
                        52. MISDEMEANOR LARCENY
                    </div>
    """  # noqa
    charge = div.select_one("div[ng-if*=ChargeOffense] div").text.strip()
    return charge.split(".", maxsplit=1)[1].strip()


@catch_parse_error
def parse_criminal_disposition(div):
    """
    Parse criminal disposition

    Sample HTML:
        <div class="roa-pad-0 roa-event-info ng-scope roa-event-info-criminal-disposition-event">
            <div ng-repeat="criminalDisposition in ::event.Event.CriminalDispositions" ng-if="::event.Event.CriminalDispositions.length &amp;&amp; !criminalDisposition.Charge.HideCharge" class="ng-scope">
                <div ng-if="::criminalDisposition.CriminalDispositionTypeId.Description" class="roa-indent-3 ng-binding ng-scope">
                    VD-Superior Dismissals w/o Leave by DA - No Plea Agreement
                </div>
    """  # noqa
    disposition = (
        div.select_one("div[ng-if*=CriminalDispositionTypeId]").text.strip().replace("\n", "")
    )
    # Remove double spaces
    return " ".join(disposition.split())
