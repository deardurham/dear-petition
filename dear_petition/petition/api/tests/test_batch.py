import pytest

from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from rest_framework import status

from dear_petition.petition.models import Batch

pytestmark = pytest.mark.django_db


def test_batch_get(api_client, batch):
    url = reverse("api:batch-detail", args=[batch.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_batch_post(api_client_anon):
    url = reverse("api:batch-list")
    response = api_client_anon.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_batch_post(api_client, fake_pdf, mock_ciprs_reader):
    mock_ciprs_reader.return_value = {"Defendant": {"Name": "Jon Doe"}}
    url = reverse("api:batch-list")
    response = api_client.post(
        url, data=MultiValueDict({"files": [fake_pdf]}), format="multipart"
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Batch.objects.get().pk == response.data["id"]
