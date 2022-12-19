import pytest

from dear_petition.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_printable_model_mixin_petition(batch, petition, contact1, contact2, offense_record1):
    """
    Test PrintableModelMixin str() and repr() methods using Petition model because Petition has many to many
    relationships.
    """

    # set many to many relationships
    petition.agencies.add(contact1)
    petition.agencies.add(contact2)
    petition.offense_records.add(offense_record1)

    # set a value greater than 50 characters to test truncation
    petition.county = "Independent and Sovereign County of Durham North Carolina"

    # assertions
    expected_str = ", ".join([
        "Petition [id=" + str(petition.id),
        "created=" + str(petition.created),
        "modified=" + str(petition.modified),
        "form_type=AOC-CR-287",
        "batch=" + str(batch.id),
        "county=Independent and Sovereign County of Durham North C...",
        "jurisdiction=D",
        "offense_records=[" + str(offense_record1.id) + "]",
        "agencies=[" + str(contact1.id) + ", " + str(contact2.id) + "]]"
    ])
    assert (str(petition) == expected_str)

    expected_repr = ", ".join([
        "{'id': " + repr(petition.id),
        "'created': " + repr(petition.created),
        "'modified': " + repr(petition.modified),
        "'form_type': 'AOC-CR-287'",
        "'batch': " + repr(batch.id),
        "'county': 'Independent and Sovereign County of Durham North Carolina'",
        "'jurisdiction': 'D'",
        "'offense_records': [" + repr(offense_record1.id) + "]",
        "'agencies': [" + repr(contact1.id) + ", " + repr(contact2.id) + "]}"
    ])
    assert (repr(petition) == expected_repr)


def test_printable_model_mixin_user():
    """
    Test PrintableModelMixin str() and repr() methods using User model because User has a field that should be excluded.
    """

    # create model object
    user = UserFactory(username="tmarshall", email="tmarshall@supremecourt.gov", name="Thurgood Marshall")

    # assertions
    expected_str = ", ".join([
        "User [id=" + str(user.id),
        "last_login=None",
        "is_superuser=False",
        "username=tmarshall",
        "first_name=",
        "last_name=",
        "email=tmarshall@supremecourt.gov",
        "is_staff=False",
        "is_active=True",
        "date_joined=" + str(user.date_joined),
        "name=Thurgood Marshall",
        "last_generated_petition_time=None",
        "groups=[]",
        "user_permissions=[]]"
    ])
    assert (str(user) == expected_str)

    expected_repr = ", ".join([
        "{'id': " + repr(user.id),
        "'last_login': None",
        "'is_superuser': False",
        "'username': 'tmarshall'",
        "'first_name': ''",
        "'last_name': ''",
        "'email': 'tmarshall@supremecourt.gov'",
        "'is_staff': False",
        "'is_active': True",
        "'date_joined': " + repr(user.date_joined),
        "'name': 'Thurgood Marshall'",
        "'last_generated_petition_time': None",
        "'groups': []",
        "'user_permissions': []}"
    ])
    assert (repr(user) == expected_repr)
