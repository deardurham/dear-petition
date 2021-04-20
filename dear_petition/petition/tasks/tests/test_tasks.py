import pytest
from unittest import mock
from datetime import timedelta

from django.utils import timezone

from dear_petition.petition import models as pm
from dear_petition.petition import constants as pc
from dear_petition.petition.tasks.clean_stale_data import clean_stale_data

pytestmark = pytest.mark.django_db


def test_clean_stale_data(batch, petition):
    assert pm.Batch.objects.all().count() == 1

    petition.created = petition.created - timedelta(hours=48, minutes=1)
    petition.save()

    num_deleted = clean_stale_data()
    assert num_deleted == 2  # 1 batch, 1 petition
    assert pm.Batch.objects.all().count() == 0
