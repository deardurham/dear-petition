import pytest

from dear_petition.petition.export.documents.advice_letter import generate_context
from dear_petition.petition.tests.factories import BatchFactory, ContactFactory

pytestmark = pytest.mark.django_db


def test_advice_letter_context():
    batch = BatchFactory(label="Faker Fakerson")
    contact = ContactFactory()

    PETITIONER_INFO = {
        "address1": "123 Fake Lane",
        "address2": "Apt F",
        "city": "Fakesville",
        "state": "NC",
        "zipCode": "99999",
    }

    EXPECTED_ADVICE_LETTER_CONTEXT = {
        "first_name": "Faker",
        "last_name": "Fakerson",
        "address": PETITIONER_INFO["address1"],
        "address_second_line": PETITIONER_INFO["address2"],
        "city": PETITIONER_INFO["city"],
        "state": PETITIONER_INFO["state"],
        "zipcode": PETITIONER_INFO["zipCode"],
        "felonies": [],
        "misdemeanors": [],
        "underaged": [],
        "dismissed": [],
        "phone_number": contact.phone_number,
        "email": contact.email,
        "attorney_name": contact.name,
    }

    context = generate_context(batch, contact, PETITIONER_INFO)
    assert context == EXPECTED_ADVICE_LETTER_CONTEXT
