from django.conf import settings
from docxtpl import DocxTemplate

from dear_petition.petition import helpers
from dear_petition.petition import models as pm
from dear_petition.petition.types.dismissed import (
    get_offense_records as get_dismissed_records,
)
from dear_petition.petition.types.underaged_convictions import (
    get_offense_records as get_underaged_conviction_records,
)

TEMPLATE = "advice_letter.docx"


def get_county_string(counties: list):
    """
    Returns string of comma separated counties given a list of counties.
    If the offense records have offenses in county1, county2, county3, this should return 'county1, county2, and county3 '
    If the offense records only have offenses in county1, it should just return 'county1 '
    """
    if len(counties) == 0:
        return ""
    elif len(counties) == 1:
        return f"{counties[0] }"
    else:
        return ", ".join(counties[0:-1]) + ", and " + counties[-1]


def generate_context(batch, attorney, client):
    context = {}
    context["first_name"], context["last_name"] = helpers.split_first_and_last_name(
        client.name
    )
    context["sex"] = batch.sex
    context["address"] = client.address1
    context["address_second_line"] = client.address2
    context["city"] = client.city
    context["state"] = client.state
    context["zipcode"] = client.zipcode

    felonies = pm.OffenseRecord.objects.filter(
        offense__ciprs_record__batch=batch, severity="FELONY"
    )
    context["felonies"] = list(felonies)

    misdemeanors = pm.OffenseRecord.objects.filter(
        offense__ciprs_record__batch=batch, severity="MISDEMEANOR"
    )
    context["misdemeanors"] = list(misdemeanors)
    conviction_counties = list(
        set(felony.county.capitalize() for felony in felonies).union(
            set(misdemeanor.county.capitalize() for misdemeanor in misdemeanors)
        )
    )
    context["conviction_counties_string"] = get_county_string(conviction_counties)
    underaged_convictions = get_underaged_conviction_records(batch)
    context["underaged"] = list(underaged_convictions)
    underaged_conviction_counties = list(
        set(
            underaged_conviction.county.capitalize()
            for underaged_conviction in underaged_convictions
        )
    )
    context["underaged_conviction_counties_string"] = get_county_string(
        underaged_conviction_counties
    )

    dismissals = get_dismissed_records(batch)
    context["dismissed"] = list(dismissals)
    dismissed_counties = list(
        set(dismissal.county.capitalize() for dismissal in dismissals)
    )
    context["dismissed_counties_string"] = get_county_string(dismissed_counties)

    context["phone_number"] = attorney.phone_number
    context["email"] = attorney.email
    context["attorney_name"] = attorney.name

    return context


def generate_advice_letter(batch):
    assert batch.client is not None and batch.attorney is not None, 'Client and attorney must be set for batch before generating document'

    context = generate_context(batch, batch.attorney, batch.client)
    doc = DocxTemplate(settings.TEMPLATE_DIR.path(TEMPLATE))
    doc.render(context)

    return doc
