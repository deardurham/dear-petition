import pytest
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from ....petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
)

pytestmark = pytest.mark.django_db


class TestBatchViewSet(TestCase):
    def setUp(self):
        self.batch_1 = BatchFactory()
        self.batch_2 = BatchFactory()
        self.batch_3 = BatchFactory()
        self.list_url = reverse("api:batch-list")
        self.detail_url = reverse("api:batch-detail", args=[self.batch_1.pk])

    def test_unauthorized(self):
        """Unauthorized users may not use the API.

        Not sending an "Authorization" header with the request to the API means
        the response will have a 401 status code.
        """

        with self.subTest("Get - List"):
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("Get - Detail"):
            response = self.client.get(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("POST"):
            data = {"code": "NEWPROJECT"}
            response = self.client.post(self.list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("PUT"):
            data = {"code": "NEWPROJECT"}
            response = self.client.put(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("PATCH"):
            data = {"code": "NEWPROJECT"}
            response = self.client.patch(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("DELETE"):
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCIPRSRecordViewSet(TestCase):
    def setUp(self):
        self.ciprsrecord_1 = CIPRSRecordFactory()
        self.ciprsrecord_2 = CIPRSRecordFactory()
        self.ciprsrecord_3 = CIPRSRecordFactory()
        self.list_url = reverse("api:ciprsrecord-list")
        self.detail_url = reverse(
            "api:ciprsrecord-detail", args=[self.ciprsrecord_1.pk]
        )

    def test_unauthorized(self):
        """Unauthorized users may not use the API.

        Not sending an "Authorization" header with the request to the API means
        the response will have a 401 status code.
        """

        with self.subTest("Get - List"):
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("Get - Detail"):
            response = self.client.get(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("POST"):
            data = {"code": "NEWPROJECT"}
            response = self.client.post(self.list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("PUT"):
            data = {"code": "NEWPROJECT"}
            response = self.client.put(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("PATCH"):
            data = {"code": "NEWPROJECT"}
            response = self.client.patch(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest("DELETE"):
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
