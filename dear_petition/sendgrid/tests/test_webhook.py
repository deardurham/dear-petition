import json
import pytest

from faker import Faker

from django.urls import reverse

from dear_petition.sendgrid.forms import EmailForm
from dear_petition.sendgrid.models import Email, Attachment

faker = Faker()


import csv
import io

from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.fixture
def attachment_file():
    output = io.StringIO("not a real PDF")
    stream = io.BytesIO(output.getvalue().encode("utf-8"))
    file_ = InMemoryUploadedFile(
        file=stream,
        field_name=None,
        name="myfile.pdf",
        content_type="pdf",
        size=stream.getbuffer().nbytes,
        charset=None,
    )
    file_.seek(0)
    return file_


@pytest.fixture
def payload():
    return {
        "from": faker.email(),
        "to": faker.email(),
        "headers": "Received: by foo.sendgrid.net with SMTP id AAA Wed, 27 Jul 2016 20:53:06 +0000 (UTC)",
        "subject": faker.sentence(),
        "text": faker.paragraph(),
        "spam_score": "0.011",
        "attachments": 0,
        "attachment-info": faker.json(),
    }


@pytest.mark.django_db
class TestWebhookView:
    def test_get_not_allowed(self, client):
        response = client.get(reverse("sendgrid-webhook"))
        assert response.status_code == 405


class TestEmails:
    def test_form_payload(self, payload, rf):
        request = rf.post(reverse("sendgrid-webhook"), data=payload)
        form = EmailForm(request)
        assert form.is_valid(), form.errors
        assert form.cleaned_data["recipient"] == payload["to"]
        assert form.cleaned_data["sender"] == payload["from"]

    @pytest.mark.django_db
    def test_email_without_attachments(self, payload, rf):
        request = rf.post(reverse("sendgrid-webhook"), data=payload)
        form = EmailForm(request)
        assert form.is_valid(), form.errors
        form.save()
        assert Email.objects.count() == 1


@pytest.mark.django_db
class TestAttachments:
    @pytest.fixture
    def request_with_files(self, rf, payload, attachment_file):
        payload["attachment-info"] = json.dumps(
            {
                "attachment2": {
                    "name": "test.pdf",
                    "type": "application/pdf",
                    "content-id": "001",
                }
            },
        )
        payload["attachment2"] = attachment_file
        return rf.post(
            reverse("sendgrid-webhook"),
            data=payload,
            # files={"attachment2": attachment_file},
        )

    def test_attachment_email_created(self, request_with_files):
        form = EmailForm(request_with_files)
        assert form.is_valid(), form.errors
        form.save()
        assert Email.objects.count() == 1

    def test_attachment_created(self, request_with_files):
        form = EmailForm(request_with_files)
        assert form.is_valid(), form.errors
        form.save()
        email = Email.objects.first()
        assert email.attachments.count() == 1
        attachment = email.attachments.first()
        assert attachment.name == "test.pdf"
