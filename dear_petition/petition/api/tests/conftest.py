from unittest import mock

import pytest

from rest_framework.test import APIClient


@pytest.fixture
def api_client_anon():
    yield APIClient()


@pytest.fixture
def api_client(api_client_anon, user):
    api_client_anon.force_authenticate(user=user)
    yield api_client_anon


@pytest.fixture
def mock_import():
    with mock.patch("dear_petition.petition.api.viewsets.import_ciprs_records") as mock_:
        batch = mock_.return_value
        batch.pk = batch.id = 99
        yield mock_
