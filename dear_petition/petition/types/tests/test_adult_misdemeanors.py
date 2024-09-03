from datetime import datetime

import pytest

from dear_petition.petition.constants import SEVERITIES, CONVICTED, CHARGED
from dear_petition.petition.models import Offense, OffenseRecord

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "action, disposition_method, severity, date, should_be_included", [
        # records that have data as they would from Portal (no action)
        ("", "District Guilty - Judge", SEVERITIES.MISDEMEANOR, datetime(2019, 8, 1), True),
        ("", "District Not Guilty - Judge", SEVERITIES.MISDEMEANOR, datetime(2019, 8, 1), False),  # exclude because not Portal guilty disposition method
        ("", "District Guilty - Judge", SEVERITIES.FELONY, datetime(2019, 8, 1), False),  # exclude because felony severity
        ("", "District Guilty - Judge", SEVERITIES.MISDEMEANOR, datetime(2024, 8, 1), False),  # exclude because too recent
        # records that have data as they would from CIPRS (disposition_method not one seen in Portal)
        (CONVICTED, "Disposed By Judge", SEVERITIES.MISDEMEANOR, datetime(2019, 8, 1), True),
        (CHARGED, "Disposed By Judge", SEVERITIES.MISDEMEANOR, datetime(2019, 8, 1), False),  # exclude because not convicted action
        (CONVICTED, "Disposed By Judge", SEVERITIES.FELONY, datetime(2019, 8, 1), False),  # exclude because felony severity
        (CONVICTED, "Disposed By Judge", SEVERITIES.MISDEMEANOR, datetime(2024, 8, 1), False),  # exclude because too recent
    ]
)
def test_adult_misdemeanors(action, disposition_method, severity, date, should_be_included, batch, record1):
    offense = Offense.objects.create(
        ciprs_record=record1,
        disposition_method=disposition_method,
        disposed_on=date,
    )
    offense_record = OffenseRecord.objects.create(
        offense=offense,
        action=action,
        severity=severity,
    )

    if should_be_included:
        assert offense_record in batch.adult_misdemeanor_records()
    else:
        assert offense_record not in batch.adult_misdemeanor_records()
