import pytz
from datetime import datetime, date


def dt_obj_to_date(dt_obj):
    """converts a datetime obj to a date"""
    return dt_obj.date()


def make_date_obj_aware(dt_obj):
    """makes datetime obj aware of timezone (EST)"""
    datetime_obj = datetime.strptime(dt_obj, "%Y-%m-%dT%H:%M:%S")
    aware_datetime_obj = datetime_obj.replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone("EST")
    )
    return aware_datetime_obj
