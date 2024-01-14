from dear_petition.portal.etl.parsers import case_summary


class TestCaseSummaryFullRecord:
    def test_parse_filno(self, soup):
        assert case_summary.parse_case_number(soup) == "01CR012345-678"

    def test_parse_county(self, soup):
        assert case_summary.parse_county(soup) == "Wake"

    def test_district_court(self, soup):
        assert case_summary.parse_court(soup) == "District"
