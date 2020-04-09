from django.utils.timezone import make_aware
import pytz
from datetime import datetime, date


def dt_obj_to_date(dt_obj):
    """converts a datetime obj to a date"""
    return dt_obj.date()


def make_datetime_aware(dt_str):
    """makes datetime string an aware datetime object (UTC ==> America/New York)"""
    datetime_obj = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
    aware_datetime_obj = make_aware(datetime_obj, timezone=pytz.utc)
    return aware_datetime_obj
