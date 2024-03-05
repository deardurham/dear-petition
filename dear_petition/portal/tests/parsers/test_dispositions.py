from dear_petition.portal.etl.parsers import dispositions


class TestDispositionsFullRecord:
    def test_parse_event_date(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert dispositions.parse_event_date(div) == "12/01/2001"

    def test_parse_event(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert dispositions.parse_event(div) == "Disposition"

    def test_parse_charge_number(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert dispositions.parse_charge_number(div) == "01"

    def test_parse_charge_offense(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert dispositions.parse_charge_offense(div) == "EXTRADITION/FUGITIVE OTH STATE"

    def test_parse_criminal_disposition(self, soup):
        div = soup.select_one(dispositions.SELECT_DISPOSITIONS)
        assert (
            dispositions.parse_criminal_disposition(div)
            == "District Dismissed by the Court - No Plea Agreement"
        )
