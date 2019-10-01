from dear_petition.petition.models import CIPRSRecord
from dear_petition.petition.forms import GeneratePetitionForm


class TestPetitionCheckboxes:
    def test_district_checkbox_value_set(self):
        record = CIPRSRecord(data={"General": {"District": "Yes"}})
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert form.record.data["General"]["District"] == "/Yes"

    def test_district_checkbox_value_not_set(self):
        record = CIPRSRecord(data={"General": {}})
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert "District" not in form.record.data["General"]

    def test_superior_checkbox_value_set(self):
        record = CIPRSRecord(data={"General": {"Superior": "Yes"}})
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert form.record.data["General"]["Superior"] == "/Yes"

    def test_superior_checkbox_value_not_set(self):
        record = CIPRSRecord(data={"General": {}})
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert "Superior" not in form.record.data["General"]

    def test_dob_clean(self):
        record = CIPRSRecord(
            data={"Defendant": {"Date of Birth/Estimated Age": "1985-01-02"}}
        )
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert (
            form.record.data["Defendant"]["Date of Birth/Estimated Age"] == "01/02/1985"
        )

    def test_dob_clean_bad(self):
        record = CIPRSRecord(
            data={"Defendant": {"Date of Birth/Estimated Age": "not a date"}}
        )
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert (
            form.record.data["Defendant"]["Date of Birth/Estimated Age"] == "not a date"
        )

    def test_offense_date_clean(self):
        record = CIPRSRecord(
            data={"Case Information": {"Offense Date": "1985-01-02T21:59:00"}}
        )
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert form.record.data["Case Information"]["Offense Date"] == "01/02/1985"

    def test_disposed_on_clean(self):
        record = CIPRSRecord(data={"Offense Record": {"Disposed On": "1985-01-02"}})
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert form.record.data["Offense Record"]["Disposed On"] == "01/02/1985"

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
        form = GeneratePetitionForm(record=record)
        form.clean()
        assert len(form.record.data["Offense Record"]["Records"]) == 1
        assert form.record.data["Offense Record"]["Records"][0]["Action"] == "CHARGED"
