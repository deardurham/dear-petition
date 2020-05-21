import io

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

from dear_petition.petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
    PetitionFactory,
    ContactFactory,
)


@pytest.fixture
def data():
    return {}


@pytest.fixture
def extra():
    return {}


@pytest.fixture
def batch(user):
    yield BatchFactory(user=user)


@pytest.fixture
def record1(batch):
    yield CIPRSRecordFactory(batch=batch, label=batch.label)


@pytest.fixture
def record2(batch):
    yield CIPRSRecordFactory(batch=batch, label=batch.label)


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
def fake_pdf2():
    return fake_file("sample2.pdf", "pdf")


@pytest.fixture
def petition(batch):
    return PetitionFactory(batch=batch)


@pytest.fixture
def contact():
    return ContactFactory()
