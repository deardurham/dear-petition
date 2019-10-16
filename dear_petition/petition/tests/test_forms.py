from dear_petition.petition.models import CIPRSRecord
from dear_petition.petition.forms import GeneratePetitionForm

from dear_petition.petition import data_dict


class TestRecordClean:
    def test_district_checkbox_value_set(self):
        record = CIPRSRecord(data={"General": {"District": "Yes"}})
        data_dict.clean(record)
        assert record.data["General"]["District"] == "/Yes"

    def test_district_checkbox_value_not_set(self):
        record = CIPRSRecord(data={"General": {}})
        data_dict.clean(record)
        assert "District" not in record.data["General"]

    def test_superior_checkbox_value_set(self):
        record = CIPRSRecord(data={"General": {"Superior": "Yes"}})
        data_dict.clean(record)
        assert record.data["General"]["Superior"] == "/Yes"

    def test_superior_checkbox_value_not_set(self):
        record = CIPRSRecord(data={"General": {}})
        data_dict.clean(record)
        assert "Superior" not in record.data["General"]

    def test_dob_clean(self):
        record = CIPRSRecord(
            data={"Defendant": {"Date of Birth/Estimated Age": "1985-01-02"}}
        )
        data_dict.clean_dob(record)
        assert record.data["Defendant"]["Date of Birth/Estimated Age"] == "01/02/1985"

    def test_dob_clean_bad(self):
        record = CIPRSRecord(
            data={"Defendant": {"Date of Birth/Estimated Age": "not a date"}}
        )
        data_dict.clean_dob(record)
        assert record.data["Defendant"]["Date of Birth/Estimated Age"] == "not a date"

    def test_offense_date_clean(self):
        record = CIPRSRecord(
            data={"Case Information": {"Offense Date": "1985-01-02T21:59:00"}}
        )
        data_dict.clean_offense_date(record)
        assert record.data["Case Information"]["Offense Date"] == "01/02/1985"

    def test_disposed_on_clean(self):
        record = CIPRSRecord(data={"Offense Record": {"Disposed On": "1985-01-02"}})
        data_dict.clean_disposed_on_date(record)
        assert record.data["Offense Record"]["Disposed On"] == "01/02/1985"

    def test_charged_offenses(self):
        data = {
            "Offense Record": {
                "Records": [
                    {"Action": "CHARGED"},
                    {"Action": "ARRAIGNED"},
                    {"Action": "CONVICTED"},
                ]
            }
        }
        record = CIPRSRecord(data=data)
        data_dict.clean_offenses(record)
        assert len(record.data["Offense Record"]["Records"]) == 1
        assert record.data["Offense Record"]["Records"][0]["Action"] == "CHARGED"
