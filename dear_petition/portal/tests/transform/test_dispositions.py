import datetime as dt
import pytest

from dear_petition.petition import constants
from dear_petition.portal.etl.models import Charge, Disposition


class TestCriminalDisposition:
    @pytest.fixture
    def disposition(self):
        return Disposition(
            event_date=dt.date(2000, 1, 1),
            event="Disposition",
            charge_number=1,
            charge_offense="BREAK OR ENTER A MOTOR VEHICLE",
            criminal_disposition="VD-District Dismissals w/o Leave by DA - No Plea Agreement",
        )

    def test_is_dismissed(self, disposition: Disposition):
        assert disposition.is_dismissed()

    def test_dismissed_transform_action(self, disposition: Disposition):
        assert disposition.transform_action() == constants.CHARGED

    def test_dismissed_transform_disposition_method(self, disposition: Disposition):
        assert (
            disposition.transform_disposition_method()
            == constants.DISTRICT_COURT_WITHOUT_DA_LEAVE
        )

    def test_not_is_dismissed(self, disposition):
        disposition.criminal_disposition = "Other"
        assert not disposition.is_dismissed()

    def test_unknown_transform_action(self, disposition: Disposition):
        disposition.criminal_disposition = "Other"
        assert disposition.transform_action() == disposition.event

    def test_unknown_transform_disposition_method(self, disposition: Disposition):
        disposition.criminal_disposition = "Other"
        assert (
            disposition.transform_disposition_method()
            == disposition.criminal_disposition
        )


class TestCharge:
    @pytest.fixture
    def charge(self):
        return Charge(
            number=1,
            offense="BREAK OR ENTER A MOTOR VEHICLE",
            statute="14-56",
            degree="FNC",
            offense_date=dt.date(1994, 2, 12),
            filed_date=dt.date(1994, 2, 14),
            arrest_date=dt.date(1994, 4, 15),
        )

    @pytest.mark.parametrize(
        "degree,severity",
        [
            ("FH", constants.SEVERITY_FELONY),
            ("FNC", constants.SEVERITY_FELONY),
            ("MNC", constants.SEVERITY_MISDEMEANOR),
        ],
    )
    def test_(self, degree: str, severity: str, charge: Charge):
        charge.degree = degree
        assert charge.transform_severity() == severity
