import io
from unittest import mock

import pytest

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.test import APIClient


@pytest.fixture
def api_client_anon():
    yield APIClient()


@pytest.fixture
def api_client(api_client_anon, user):
    api_client_anon.force_authenticate(user=user)
    yield api_client_anon


def fake_file(filename, content_type):
    output = io.StringIO("blahblah")
    stream = io.BytesIO(output.getvalue().encode("utf-8"))
    file_ = InMemoryUploadedFile(
        file=stream,
        field_name=None,
        name=filename,
        content_type=content_type,
        size=stream.getbuffer().nbytes,
        charset=None,
    )
    return file_


@pytest.fixture
def fake_pdf():
    return fake_file("sample.pdf", "pdf")


@pytest.fixture
def mock_ciprs_reader():
    with mock.patch("dear_petition.petition.etl.load.parse_ciprs_document") as mock_:
        yield mock_
