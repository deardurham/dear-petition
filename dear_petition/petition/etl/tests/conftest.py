from unittest import mock

import pytest


@pytest.fixture
def mock_ciprs_reader():
    with mock.patch("dear_petition.petition.etl.load.parse_ciprs_document") as mock_:
        yield mock_
