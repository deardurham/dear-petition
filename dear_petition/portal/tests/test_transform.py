import datetime as dt

from dear_petition.portal.etl.models import Disposition


class TestCriminalDisposition:
    def test_is_dismissed(self):
        assert Disposition(
            event_date=dt.date(2000, 1, 1),
            event="Disposition",
            charge_number=1,
            charge_offense="BREAK OR ENTER A MOTOR VEHICLE",
            criminal_disposition="VD-District Dismissals w/o Leave by DA - No Plea Agreement",
        ).is_dismissed()

    def test_not_is_dismissed(self):
        assert not Disposition(
            event_date=dt.date(2000, 1, 1),
            event="Disposition",
            charge_number=1,
            charge_offense="BREAK OR ENTER A MOTOR VEHICLE",
            criminal_disposition="District Guilty - Judge",
        ).is_dismissed()
