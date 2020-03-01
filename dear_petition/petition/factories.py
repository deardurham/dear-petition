import logging
from datetime import datetime

import factory

import dear_petition.petition.models as models
import dear_petition.users.models as user_model

logger = logging.getLogger(__name__)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = user_model.User
        strategy = factory.BUILD_STRATEGY

    name = "John Test"

class BatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Batch
        strategy = factory.BUILD_STRATEGY

    user = factory.SubFactory(UserFactory)

class CIPRSRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CIPRSRecord
        strategy = factory.BUILD_STRATEGY
    
    batch = factory.SubFactory(BatchFactory)
    data = {}