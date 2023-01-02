import factory

from dear_petition.sendgrid.models import Email, Attachment


class EmailFactory(factory.DjangoModelFactory):

    subject = factory.Faker("sentence")
    recipient = factory.Faker("ascii_company_email")
    sender = factory.Faker("ascii_company_email")
    payload = factory.Faker("pydict", allowed_types=["str", "int"])

    class Meta:
        model = Email


class AttachmentFactory(factory.DjangoModelFactory):

    name = factory.Faker("file_name")
    type = factory.Faker("mime_type")
    file = factory.Faker("file_path", absolute=False)
    email = factory.SubFactory(EmailFactory)

    class Meta:
        model = Attachment
