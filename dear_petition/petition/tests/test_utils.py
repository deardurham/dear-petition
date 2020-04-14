import pytest
import pytz
from django.conf import settings
from datetime import datetime, date
from ..utils import (
    dt_obj_to_date,
    make_datetime_aware,
)
from ..constants import DATETIME_FORMAT


def test_dt_obj_to_date():
    """Should receive only datetime objects to be converted into dates
    """
    dt_obj = datetime.now()
    date_obj = dt_obj_to_date(dt_obj)
    assert isinstance(date_obj, (date,))
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


def test_make_datetime_aware():
    """Aware Datetime should be returned unless dt_str is empty ("" or None)
    """
    dt_str = ""
    aware_dt = make_datetime_aware(dt_str)
    assert aware_dt == None
    dt_str = None
    aware_dt = make_datetime_aware(dt_str)
    assert aware_dt == None
    dt_str = datetime.now().strftime(DATETIME_FORMAT)
    aware_dt = make_datetime_aware(dt_str)
    datetime_obj = datetime.strptime(dt_str, DATETIME_FORMAT)
    aware_datetime_obj = datetime_obj.astimezone(pytz.timezone(settings.TIME_ZONE))
    assert aware_dt == aware_datetime_obj
