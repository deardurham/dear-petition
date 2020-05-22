import io

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile

from dear_petition.petition.tests.factories import (
    BatchFactory,
    CIPRSRecordFactory,
    PetitionFactory,
    OffenseFactory,
    OffenseRecordFactory,
)
from dear_petition.petition.types import dismissed


@pytest.fixture
def data():
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
def dismissed_offense(record1):
    return OffenseFactory(
        disposition_method=dismissed.DISPOSITION_METHODS[0], ciprs_record=record1
    )


@pytest.fixture
def non_dismissed_offense(record1):
    return OffenseFactory(disposition_method="OTHER", ciprs_record=record1)


@pytest.fixture
def charged_dismissed_record(dismissed_offense):
    return OffenseRecordFactory(action="CHARGED", offense=dismissed_offense)
