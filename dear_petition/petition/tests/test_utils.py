import pytz
import pytest
from django.utils.timezone import make_aware, utc
from datetime import datetime, date

from dear_petition.petition import utils as pu

from ..constants import DATETIME_FORMAT

pytestmark = pytest.mark.django_db


def test_dt_obj_to_date(settings):
    """Should receive only datetime objects to be converted into dates"""
    # Set the TIME_ZONE in the settings.
    settings.TIME_ZONE = "America/New_York"

    # A datetime that refers to 20:00 on January 1, 2018 in New York.
    datetime_2018_01_01_2000_ny = make_aware(
        datetime(year=2018, month=1, day=1, hour=20, minute=0, second=0),
        timezone=pytz.timezone("America/New_York"),
    )
    # A datetime that refers to 01:00 on January 2, 2018 in UTC. Note: this is
    # the same exact moment in time as datetime_2018_01_01_2000_ny.
    datetime_2018_01_02_0100_utc = make_aware(
        datetime(year=2018, month=1, day=2, hour=1, minute=0, second=0),
        timezone=pytz.utc,
    )
    # Calling pu.dt_obj_to_date() returns the date at each of these moments in the
    # "America/New_York" timezone, which was "2018-01-01".
    assert pu.dt_obj_to_date(datetime_2018_01_01_2000_ny) == date(year=2018, month=1, day=1)
    assert pu.dt_obj_to_date(datetime_2018_01_02_0100_utc) == date(year=2018, month=1, day=1)

    # Calling pu.dt_obj_to_date() for non datetime objects returns None.
    dt_obj = "A random string."
    date_obj = pu.dt_obj_to_date(dt_obj)
    assert date_obj == None
    dt_obj = 123438
    date_obj = pu.dt_obj_to_date(dt_obj)
    assert date_obj == None
    dt_obj = {"dict": "random dict"}
    date_obj = pu.dt_obj_to_date(dt_obj)
    assert date_obj == None
    dt_obj = None
    date_obj = pu.dt_obj_to_date(dt_obj)
    assert date_obj == None


def test_make_datetime_aware(settings):
    """Aware Datetime should be returned unless dt_str is empty ("" or None)"""
    # Set the TIME_ZONE in the settings.
    settings.TIME_ZONE = "America/New_York"

    # Calling pu.make_datetime_aware() returns a timezone-aware datetime referring
    # to the moment from the naive_datetime_obj, in the appropriate time zone.
    naive_datetime_str = "2018-01-01T20:00:00"
    expected_datetime_obj = make_aware(
        datetime(year=2018, month=1, day=1, hour=20, minute=0, second=0),
        timezone=pytz.timezone("America/New_York"),
    )
    assert pu.make_datetime_aware(naive_datetime_str) == expected_datetime_obj

    # Calling pu.make_datetime_aware() for non-datetime strings returns None.
    dt_str = ""
    aware_dt = pu.make_datetime_aware(dt_str)
    assert aware_dt == None
    dt_str = None
    aware_dt = pu.make_datetime_aware(dt_str)
    assert aware_dt == None


def test_make_datetime_aware_ambiguous(settings):
    """Aware Datetime should be returned assuming standard time in the case of ambiguity between standard time and
    daylight saving time.
    """
    # Set the TIME_ZONE in the settings.
    settings.TIME_ZONE = "America/New_York"

    # Calling pu.make_datetime_aware() with a date/time that falls within the hour before or after daylight saving time
    # ends returns a timezone-aware datetime referring to the moment from the naive_datetime_obj, in the appropriate
    # time zone, assuming standard time.
    naive_datetime_str = "2011-11-06T01:46:00"
    expected_datetime_obj = make_aware(
        datetime(year=2011, month=11, day=6, hour=1, minute=46, second=0),
        timezone=pytz.timezone("America/New_York"),
        is_dst=False,
    )
    assert pu.make_datetime_aware(naive_datetime_str) == expected_datetime_obj


def test_format_petition_date(settings):
    """Should return %m/%d/%Y date. If it is non-EST datetime, it will convert to EST first."""

    date = datetime(year=2020, month=1, day=1, hour=11, minute=59, second=0, tzinfo=utc)
    assert pu.format_petition_date(date) == "01/01/2020"


def test_get_text_pixel_length():
    text = "m"
    assert pu.get_text_pixel_length(text) == 10


def test_get_truncation_point_of_text_by_pixel_size():
    text = "This is an example line of text...er...I mean...lorem ipsum?"
    truncation_point = pu.get_truncation_point_of_text_by_pixel_size(text, 200)
    assert truncation_point == 42


def test_get_truncation_point_of_short_text_by_pixel_size():
    """When the full text is shorter than the desired truncation point, it should just return the whole string."""
    text = "Lorem ipsum"
    truncation_point = pu.get_truncation_point_of_text_by_pixel_size(text, 20000)
    assert truncation_point == len(text)


def test_get_petition_filename(petition):
    petition.created = datetime(2024, 7, 28, 0, 0)
    petition.save()
    petitioner_name = "Test"
    assert (
        pu.get_petition_filename(petitioner_name, petition, "pdf")
        == "07-28-2024 DURHAM DC 146(a) Test.pdf"
    )
