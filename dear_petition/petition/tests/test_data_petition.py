from dear_petition.petition.models import DataPetition


def test_data_petition():
    petition = DataPetition(form_type="sample")
    assert petition.data_only
