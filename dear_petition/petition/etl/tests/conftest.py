from unittest import mock

import pytest


@pytest.fixture
def mock_ciprs_reader():
    with mock.patch("dear_petition.petition.etl.load.parse_ciprs_document") as mock_:
        yield mock_


@pytest.fixture
def mock_transform_ciprs_document():
    with mock.patch(
        "dear_petition.petition.etl.extract.transform_ciprs_document"
    ) as mock_:
        yield mock_
