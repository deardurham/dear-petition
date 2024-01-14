from dear_petition.portal.etl.parsers import party_info


class TestPartyInfoFullRecord:
    def test_parse_defendant_name(self, soup):
        assert party_info.parse_defendant_name(soup) == "DOE, JANE EMMA"
