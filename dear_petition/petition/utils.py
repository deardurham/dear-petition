import logging
import pytz
from datetime import datetime
from django.conf import settings
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import IntegerField, Case, When, Value
from django.db.models.functions import Cast, Substr, Concat
from .constants import DATE_FORMAT

from PIL import ImageFont
import dateutil.parser

logger = logging.getLogger(__name__)


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
    according to DATE_FORMAT, else this definition will return
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


def split_first_and_last_name(name):
    names = name.split(" ")

    if len(names) == 1:
        return name, None

    first_name = names[0].capitalize()
    last_name = names[-1].capitalize()
    return first_name, last_name


def get_285_form_agency_address(agency):
    """The 285 box has a giant text box where all the agency information goes"""
    body = ""
    for field_name in [
        "name",
        "address1",
        "address2",
        "city",
        "state",
        "zipcode",
    ]:
        field = getattr(agency, field_name)
        body += f"{field}\n"

    return body


def get_text_pixel_length(text):
    """
    Given a string, will give it's length in pixels.
    Note that this may vary by operating system due to different font rendering engines.
    Note also that the length of a multi-character string may not equal the sum of the length of the characters comprising the string. This is again due to font rendering.
    """
    font = ImageFont.truetype(str(settings.APPS_DIR.path("static/times.ttf")), size=12)
    size = font.getsize(text)
    return size[0]


def get_truncation_point_of_text_by_pixel_size(text, desired_length):
    """
    Given a string and a desired pixel length, will return the index the string needs to be truncated to obtain the the maximal string that can fit within the desired length
    """
    letter_lengths = {}

    def calculate_letter_length(letter):
        if letter in letter_lengths:
            return letter_lengths[letter]
        letter_length = get_text_pixel_length(letter)
        letter_lengths[letter] = letter_length
        return letter_length

    truncated_string_size = 0
    idx = 0
    text_length = len(text)
    while idx < text_length:
        next_letter = text[idx]
        letter_length = calculate_letter_length(next_letter)
        truncated_string_size += letter_length
        if truncated_string_size > desired_length:
            break
        else:
            idx += 1

    return idx


def get_ordered_offense_records(petition_document):
    # When sorting these, need to interpret first 2 digits of file number as year and sort based on that
    two_digit_current_year = timezone.now().year % 2000  # Returns 21 given 2021
    qs = (
        petition_document.offense_records.filter(petitionoffenserecord__active=True)
        .select_related("offense__ciprs_record")
        .annotate(
            first_two_digits_file_number_chars=Substr(
                "offense__ciprs_record__file_no", 1, 2
            )
        )
        .annotate(
            first_two_digits_file_number=Cast(
                "first_two_digits_file_number_chars", output_field=IntegerField()
            )
        )
        .annotate(
            file_number_year=Case(
                When(
                    first_two_digits_file_number__gt=two_digit_current_year,
                    then=Concat(Value("19"), "first_two_digits_file_number_chars"),
                ),
                When(
                    first_two_digits_file_number__lte=two_digit_current_year,
                    then=Concat(Value("20"), "first_two_digits_file_number_chars"),
                ),
            )
        )
        .order_by(
            "file_number_year",
            "offense__ciprs_record__file_no",
            "pk",
        )
    )

    return qs
def resolve_dob(qs):
    """
    It is possible that different CIPRS records could have different dates of birth. In this case, use the earliest date of birth as it is the most conservative.
    """
    dobs = set(
        qs.filter(offense__ciprs_record__dob__isnull=False).values_list(
            "offense__ciprs_record__dob"
        )
    )

    if not dobs:
        return None

    earliest_dob = min(dobs)[0]
    if len(dobs) > 1:
        logger.warning(
            f"This batch has multiple birthdates. Using the earliest birthdate {earliest_dob}"
        )

    return earliest_dob
