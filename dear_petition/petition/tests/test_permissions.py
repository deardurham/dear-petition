import pytest

import dear_petition.petition.tests.factories as factories
import dear_petition.petition.permissions as permissions

pytestmark = pytest.mark.django_db

class TestPermissions:

    def test_is_owner(self,batch):
        assert permissions.is_owner(batch.user, batch) == True

    def test_is_not_owner(self,user,batch):
        assert not permissions.is_owner(user, batch) == True