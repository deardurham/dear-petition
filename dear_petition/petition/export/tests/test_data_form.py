import pytest

from dear_petition.petition import constants
from dear_petition.petition.models import DataPetition
from dear_petition.petition.export.forms import DataPetitionForm


@pytest.fixture
def petition():
    return DataPetition(form_type=constants.DISMISSED)


@pytest.fixture
def form(petition, extra):
    return DataPetitionForm(petition, extra)


def test_context(form):
    form.extra = {"foo", "bar"}
    form.build_form_context()
    assert form.data == form.extra
