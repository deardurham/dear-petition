from django.utils.timezone import make_aware
import pytz
from datetime import datetime, date


def dt_obj_to_date(dt_obj):
    """converts a datetime obj to a date"""
    return dt_obj.date()


def make_datetime_aware(dt_str):
    """makes datetime string an aware datetime object (UTC ==> America/New York)"""
    if dt_str is None or dt_str == "":
        return None
    datetime_obj = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
    aware_datetime_obj = datetime_obj.replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone("America/New_York")
    )
    return aware_datetime_obj
