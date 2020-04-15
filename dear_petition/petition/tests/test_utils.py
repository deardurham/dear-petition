import pytest
from pytest_django.fixtures import settings
import pytz
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime, date
from ..utils import dt_obj_to_date, make_datetime_aware
from ..constants import DATETIME_FORMAT


def test_dt_obj_to_date(settings):
    """Should receive only datetime objects to be converted into dates
    """
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
    # Calling dt_obj_to_date() returns the date at each of these moments in the
    # "America/New_York" timezone, which was "2018-01-01".
    assert dt_obj_to_date(datetime_2018_01_01_2000_ny) == date(
        year=2018, month=1, day=1
    )
    assert dt_obj_to_date(datetime_2018_01_02_0100_utc) == date(
        year=2018, month=1, day=1
    )

    # Calling dt_obj_to_date() for non datetime objects returns None.
    dt_obj = "A random string."
    date_obj = dt_obj_to_date(dt_obj)
    assert date_obj == None
    dt_obj = 123438
    date_obj = dt_obj_to_date(dt_obj)
    assert date_obj == None
    dt_obj = {"dict": "random dict"}
    date_obj = dt_obj_to_date(dt_obj)
    assert date_obj == None
    dt_obj = None
    date_obj = dt_obj_to_date(dt_obj)
    assert date_obj == None


def test_make_datetime_aware(settings):
    """Aware Datetime should be returned unless dt_str is empty ("" or None)
    """
    # Set the TIME_ZONE in the settings.
    settings.TIME_ZONE = "America/New_York"

    # Calling make_datetime_aware() returns a timezone-aware datetime referring
    # to the moment from the naive_datetime_obj, in the appropriate time zone.
    naive_datetime_str = "2018-01-01T20:00:00"
    expected_datetime_obj = make_aware(
        datetime(year=2018, month=1, day=1, hour=20, minute=0, second=0),
        timezone=pytz.timezone("America/New_York"),
    )
    assert make_datetime_aware(naive_datetime_str) == expected_datetime_obj

    # Calling make_datetime_aware() for non-datetime strings returns None.
    dt_str = ""
    aware_dt = make_datetime_aware(dt_str)
    assert aware_dt == None
    dt_str = None
    aware_dt = make_datetime_aware(dt_str)
    assert aware_dt == None
