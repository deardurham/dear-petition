import pytest

from dear_petition.petition import constants
from dear_petition.petition.models import DataPetition, DataPetitionDocument
from dear_petition.petition.export.forms import DataPetitionForm


@pytest.fixture
def petition():
    return DataPetition(form_type=constants.DISMISSED)


@pytest.fixture
def petition_document(petition):
    return DataPetitionDocument(petition=petition)


@pytest.fixture
def form(petition_document, extra):
    return DataPetitionForm(petition_document, extra)


def test_context(form):
    form.extra = {"foo", "bar"}
    form.build_form_context()
    assert form.data == form.extra
