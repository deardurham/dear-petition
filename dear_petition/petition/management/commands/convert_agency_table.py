import re

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from dear_petition.petition import models

def convert_contacts_to_agency_objects(current_cls, target_cls):
    # Migrate from Contact model to Agency model
    agency_contacts = current_cls.objects.filter(category='agency')
    print()
    for agency_contact in agency_contacts.values():
        with transaction.atomic():
            id = agency_contact.pop('id')
            agency = target_cls(**agency_contact)
            if re.search(models.AGENCY_SHERRIFF_OFFICE_PATTERN, agency.name, re.IGNORECASE) or re.search(models.AGENCY_SHERRIFF_DEPARTMENT_PATTERN, agency.name, re.IGNORECASE):
                agency.is_sheriff = True
            else:
                agency.is_sheriff = False
            agency.save()

            current_cls.objects.filter(id=id).delete()
            print(f"Migrated Contact '{agency.name}' to Agency table")
    print()

"""
# attempt to provide backwards migration for agencies, but it doesn't seem worth the effort
def convert_agencies_to_contact_objects(current_cls, target_cls):
    # convert agency contacts to actual agency objects then delete the contact
    agency_objects = current_cls.objects.all()
    print()
    for agency_object in agency_objects.values():
        with transaction.atomic():
            id = agency_object.pop('id')
            agency_object.pop('contact_ptr_id')
            agency_object.pop('is_sheriff')
            agency_contact = target_cls(**agency_object)
            agency_contact.save()

            current_cls.objects.filter(id=id).delete()
            print(f"Migrated Agency '{agency_contact.name}' to Contact table")
    print()
"""


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--convert_contacts", action="store_true", help="Convert existing agencies in Contact table to Agency table")
        parser.add_argument("--convert_agencies", action="store_true", help="Convert existing agencies in Agency table to Contact table")

    def handle(self, *args, **options):
        if options["convert_contacts"]:
            convert_contacts_to_agency_objects()
        elif options["convert_agencies"]:
            convert_agencies_to_contact_objects()
        else:
            raise CommandError('Did not provide one of `convert_contacts` or `convert_agencies` arguments')