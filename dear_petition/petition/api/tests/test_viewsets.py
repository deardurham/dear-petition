from datetime import timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from dear_petition.users.tests.factories import UserFactory

from ....petition.tests.factories import BatchFactory, CIPRSRecordFactory

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
        self.other_user = UserFactory()
        self.batch_1 = BatchFactory(user=self.user)
        self.batch_2 = BatchFactory(user=self.user)
        self.batch_3 = BatchFactory(user=self.user)
        self.batch_4 = BatchFactory(user=self.other_user)
        self.batch_5 = BatchFactory(user=self.other_user)
        self.list_url = reverse("api:batch-list")
        self.detail_url = reverse("api:batch-detail", args=[self.batch_1.pk])
        # Create a token for the self.user, to be used with each request.
        self.tokens = get_tokens_for_user(self.user)
        self.access = self.tokens["access"]
        # other user's tokens and access token
        self.other_user_tokens = get_tokens_for_user(self.other_user)
        self.other_user_access = self.other_user_tokens["access"]

    def test_user_permissions(self):
        batch_list_user_owns = [self.batch_1, self.batch_2, self.batch_3]
        batch_list_user_owns_labels = [batch.label for batch in batch_list_user_owns]
        batch_list_other_user_owns = [self.batch_4, self.batch_5]
        batch_list_other_user_owns_labels = [
            batch.label for batch in batch_list_other_user_owns
        ]
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        # assert that the result count equals the amount of batches the user owns
        self.assertEqual(response.data["count"], len(batch_list_user_owns))
        results = [dict(batch) for batch in response.data["results"]]
        result_labels = [batch["label"] for batch in results]
        for label in result_labels:
            # assert that the result contains labels that the user owns
            self.assertIn(label, batch_list_user_owns_labels)
            # assert that the result does not contain labels that the other user owns
            self.assertNotIn(label, batch_list_other_user_owns_labels)

    def test_superuser_permissions(self):
        self.user.is_superuser = True
        self.user.save()
        batch_list_for_superuser = [
            self.batch_1,
            self.batch_2,
            self.batch_3,
            self.batch_4,
            self.batch_5,
        ]
        batch_list_for_superuser_labels = [
            batch.label for batch in batch_list_for_superuser
        ]
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        # assert that the result count equals the amount of batches the superuser "owns"
        self.assertEqual(response.data["count"], len(batch_list_for_superuser))
        results = [dict(batch) for batch in response.data["results"]]
        result_labels = [batch["label"] for batch in results]
        for label in result_labels:
            # assert that the result contains labels that the superuser "owns"
            self.assertIn(label, batch_list_for_superuser_labels)

    def test_authorized(self):
        with self.subTest("Get - List"):
            batch_list = [self.batch_1, self.batch_2, self.batch_3]
            self.client.cookies[settings.AUTH_COOKIE_KEY] = self.access

            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], len(batch_list))
            results = [dict(batch) for batch in response.data["results"]]
            result_labels = [batch["label"] for batch in results]
            batch_list_labels = [batch.label for batch in batch_list]
            for bl in batch_list_labels:
                self.assertIn(bl, result_labels)

        with self.subTest("Get - Detail"):
            response = self.client.get(
                self.detail_url, HTTP_AUTHORIZATION=f"Bearer {self.access}"
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.batch_1.label, response.data["label"])

        with self.subTest("POST"):
            data = dict(
                batch=self.batch_1,
                label="Homer Simpson",
                date_uploaded=self.batch_1.date_uploaded,
                user=self.user.pk,
            )
            response = self.client.post(
                self.list_url, data=data, HTTP_AUTHORIZATION=f"Bearer {self.access}"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with self.subTest("PUT"):
            pass

        with self.subTest("PATCH"):
            pass

        with self.subTest("DELETE"):
            response = self.client.delete(
                self.detail_url, HTTP_AUTHORIZATION=f"Bearer {self.access}"
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized(self):
        """Unauthorized users may not use the API.

        Not sending an "Authorization" header with the request to the API means
        the response will have a 401 status code.
        """

        with self.subTest("Get - List"):
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest("Get - Detail"):
            response = self.client.get(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest("POST"):
            data = {"code": "NEWPROJECT"}
            response = self.client.post(self.list_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest("PUT"):
            data = {"code": "NEWPROJECT"}
            response = self.client.put(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest("PATCH"):
            data = {"code": "NEWPROJECT"}
            response = self.client.patch(self.detail_url, data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest("DELETE"):
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
