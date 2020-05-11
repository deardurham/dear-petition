import pytest
from datetime import timedelta

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

from dear_petition.users.tests.factories import UserFactory

from ....petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
)

pytestmark = pytest.mark.django_db


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class TestBatchViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.batch_1 = BatchFactory()
        self.batch_2 = BatchFactory()
        self.batch_3 = BatchFactory()
        self.batch_list = [self.batch_1, self.batch_2, self.batch_3]
        self.list_url = reverse("api:batch-list")
        self.detail_url = reverse("api:batch-detail", args=[self.batch_1.pk])
        # Create a token for the self.user, to be used with each request.
        self.tokens = get_tokens_for_user(self.user)
        self.access = self.tokens["access"]

    def test_authorized(self):
        with self.subTest("Get - List"):
            response = self.client.get(
                self.list_url, HTTP_AUTHORIZATION=f"Bearer {self.access}"
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

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


class TestCIPRSRecordViewSet(APITestCase):
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
