import pytest

from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from rest_framework import status

pytestmark = pytest.mark.django_db


def test_unauthorized_batch_post(api_client_anon):
    response = api_client_anon.post(reverse("api:batch-list"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_batch_post_file(api_client, fake_pdf, mock_import):
    """Test POST functionality w/o testing actual ETL."""
    data = {"files": [fake_pdf]}
    response = api_client.post(reverse("api:batch-list"), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert mock_import.assert_called_once
    assert "id" in response.data


def test_batch_post_multiple_files(api_client, fake_pdf, fake_pdf2, mock_import):
    """Test POST with multiple files functionality w/o testing actual ETL."""
    data = {"files": [fake_pdf, fake_pdf2]}
    response = api_client.post(reverse("api:batch-list"), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert mock_import.assert_called_once
    assert "id" in response.data
