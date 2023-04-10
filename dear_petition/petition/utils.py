import pytz
from datetime import datetime
from django.conf import settings
from django.utils.timezone import make_aware
from django.utils import timezone
from .constants import DATE_FORMAT


import dateutil.parser


def dt_obj_to_date(dt_obj):
    """
    Convert a datetime obj to a date.

    More technically, this function converts a datetime object to the date in the
    settings.TIME_ZONE at the exact moment that the datetime object refers to.
    For example, if dt_obj = datetime.datetime(2018, 1, 2, 1, 0, tzinfo=<UTC>),
    then dt_obj refers to the moment that it was 01:00 in the UTC timezone on
    January 2, 2018. If this project has settings.TIME_ZONE set to "America/New_York",
    then at this moment in time would be 20:00 on January 1, 2018 in New York. As
    a result, this function would return "2018-01-01".
    """
    if isinstance(dt_obj, (datetime,)):
        return dt_obj.astimezone(pytz.timezone(settings.TIME_ZONE)).date()
    return None


def make_datetime_aware(dt_str):
    """
    Take a datetime string in DATETIME_FORMAT and return a timezone-aware datetime object.

    Note: we assume that we receive a datetime string like "2018-01-01T20:00:00",
    which does not have a timezone attached to it, and that it refers to a datetime
    in the settings.TIME_ZONE.
    The steps we take are:
      a) turn the datetime string into a timezone-naive datetime object
      b) assign the timezone-naive datetime a timezone based on settings.TIME_ZONE
    """
    if dt_str is None or dt_str == "":
        return None
    # a) Turn the datetime string into a timezone-naive datetime object
    naive_datetime_obj = dateutil.parser.parse(dt_str)

    # b) Assign the timezone-naive datetime a timezone based on settings.TIME_ZONE
    aware_datetime_obj = make_aware(
        naive_datetime_obj, pytz.timezone(settings.TIME_ZONE)
    )
    # Return the timezone aware object.
    return aware_datetime_obj


def format_petition_date(date):
    """Format Date Objects for PDF Writer

    If date is true then the date object will be formatted
    according to DATE_FORMAT, else this defintion will return
    empty strings. Both of which can be written to the PDF
    correctly.
    """

    if isinstance(date, datetime):
        date = date.astimezone(pytz.timezone(settings.TIME_ZONE))
    return date.strftime(DATE_FORMAT) if date else ""


# https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def get_petition_filename(petitioner_name, petition, extension, addendum_document=None):
    form_type = (
        f"{petition.form_type} {addendum_document.form_type}"
        if addendum_document is not None
        else petition.form_type
    )
    return f"{petitioner_name} - {form_type} - {petition.jurisdiction} {petition.county}.{extension}"
