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
