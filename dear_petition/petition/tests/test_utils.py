import pytest
from datetime import datetime, date
from ..utils import (
    dt_obj_to_date,
    make_datetime_aware,
)


def test_make_datetime_aware():
    # In the event that the
    dt_str = ""
    aware_dt = make_datetime_aware(dt_str)
    assert aware_dt == None
    dt_str = None
    aware_dt = make_datetime_aware(dt_str)
    dt_str = None
    dt_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    aware_dt = make_datetime_aware(dt_str)
