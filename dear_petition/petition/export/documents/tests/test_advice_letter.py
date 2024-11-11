import pytest

from dear_petition.petition.export.documents.advice_letter import generate_context
from dear_petition.petition.tests.factories import (
    AttorneyFactory,
    BatchFactory,
    ClientFactory,
    CIPRSRecordFactory,
)

pytestmark = pytest.mark.django_db


def test_advice_letter_context():
    batch = BatchFactory()
    CIPRSRecordFactory(batch=batch, sex="M")

    PETITIONER_INFO = {
        "name": "Faker Fakerson",
        "address1": "123 Fake Lane",
        "address2": "Apt F",
        "city": "Fakesville",
        "state": "NC",
        "zipcode": "99999",
    }
    client = ClientFactory(**PETITIONER_INFO)

    ATTORNEY_INFO = {
        "name": "Attorney Name",
        "address1": "234 Fake Street",
        "address2": "Apt 101",
        "city": "Faketown",
        "state": "NC",
        "zipcode": "11111",
        "phone_number": "123-456-7890",
        "email": "attorney@example.com",
    }
    attorney = AttorneyFactory(**ATTORNEY_INFO)

    EXPECTED_ADVICE_LETTER_CONTEXT = {
        "first_name": "Faker",
        "last_name": "Fakerson",
        "sex": "M",
        "address": PETITIONER_INFO["address1"],
        "address_second_line": PETITIONER_INFO["address2"],
        "city": PETITIONER_INFO["city"],
        "state": PETITIONER_INFO["state"],
        "zipcode": PETITIONER_INFO["zipcode"],
        "felonies": [],
        "misdemeanors": [],
        "conviction_counties_string": "",
        "underaged": [],
        "underaged_conviction_counties_string": "",
        "dismissed": [],
        "dismissed_counties_string": "",
        "phone_number": ATTORNEY_INFO["phone_number"],
        "email": ATTORNEY_INFO["email"],
        "attorney_name": ATTORNEY_INFO["name"],
    }

    context = generate_context(batch, attorney, client)
    assert context == EXPECTED_ADVICE_LETTER_CONTEXT
