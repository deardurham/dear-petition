from django.contrib.admin import AdminSite

from dear_petition.petition.admin import GeneratedPetitionAdmin
from dear_petition.petition.models import GeneratedPetition


class MockRequest:
    pass


request = MockRequest()


def test_generated_petition_admin():
    # test constants
    READ_ONLY_FIELDS = [
        "username",
        "batch_id",
        "form_type",
        "number_of_charges",
        "county",
        "jurisdiction",
        "race",
        "sex",
        "age",
    ]
    READ_WRITE_FIELDS = []  # there are currently no writable fields in GeneratedPetitionAdmin

    # create GeneratedPetitionAdmin
    gp_admin = GeneratedPetitionAdmin(GeneratedPetition, AdminSite())

    # assertions
    assert list(gp_admin.get_form(request).base_fields) == READ_WRITE_FIELDS
    assert list(gp_admin.get_fields(request)) == READ_WRITE_FIELDS + READ_ONLY_FIELDS
    assert list(gp_admin.get_fieldsets(request)) == [
        (None, {"fields": READ_WRITE_FIELDS + READ_ONLY_FIELDS})
    ]
