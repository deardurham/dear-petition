import pytz
from datetime import datetime, date
from django.conf import settings
from django.utils.timezone import make_aware
from .constants import DATETIME_FORMAT


def dt_obj_to_date(dt_obj):
    """converts a datetime obj to a date"""
    if isinstance(dt_obj, (datetime,)):
        return dt_obj.date()
    return None


def make_datetime_aware(dt_str):
    """makes datetime string an aware datetime object (UTC ==> America/New York)"""
    if dt_str is None or dt_str == "":
        return None
    datetime_obj = datetime.strptime(dt_str, DATETIME_FORMAT)
    aware_datetime_obj = datetime_obj.astimezone(pytz.timezone(settings.TIME_ZONE))
    return aware_datetime_obj
