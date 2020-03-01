import pytest

import dear_petition.petition.factories as factories
import dear_petition.petition.permissions as permissions

class TestPermissions:

   
    @pytest.fixture
    def batch(self):
        return factories.BatchFactory()

    @pytest.fixture
    def user(self):
        return factories.UserFactory()

    def test_is_owner(self,batch):
        assert permissions.is_owner(batch.user, batch) == True

    def test_is_not_owner(self,user,batch):
        assert not permissions.is_owner(user, batch) == True