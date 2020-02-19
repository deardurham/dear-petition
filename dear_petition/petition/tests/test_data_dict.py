import pytest

from dear_petition.petition.data_dict import map_data

pytestmark = pytest.mark.django_db


def test_most_recent_record_none(batch):
    with pytest.raises(ValueError):
        assert map_data({}, batch)
