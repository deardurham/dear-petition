import io
import json
import pytest

from faker import Faker

from django.urls import reverse

from dear_petition.sendgrid.forms import EmailForm
from dear_petition.sendgrid.models import Email
from dear_petition.sendgrid.views import email_is_allowed, webhook

from django.core.files.uploadedfile import InMemoryUploadedFile

faker = Faker()


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
    def test_email_with_empty_subject(self, payload, rf):
        payload['subject'] = ''
        request = rf.post(reverse("sendgrid-webhook"), data=payload)
        form = EmailForm(request)
        assert form.is_valid(), form.errors
        form.save()
        assert Email.objects.count() == 1

    @pytest.mark.django_db
    def test_email_without_subject(self, payload, rf):
        payload.pop('subject')
        request = rf.post(reverse("sendgrid-webhook"), data=payload)
        form = EmailForm(request)
        assert form.is_valid(), form.errors
        form.save()
        assert Email.objects.count() == 1

    @pytest.mark.django_db
    def test_sender_allowed(self, settings, rf, payload):
        """Emails should be saved from allowed senders"""
        payload["from"] = "user@example.com"
        settings.SENDGRID_ALLOWED_SENDERS = ["example.com"]
        request = rf.post(reverse("sendgrid-webhook"), data=payload)
        response = webhook(request)
        assert response.status_code == 201
        assert Email.objects.count() == 1

    @pytest.mark.django_db
    def test_sender_not_allowed(self, settings, rf, payload):
        """Emails should NOT be saved from unknown senders"""
        payload["from"] = "nope@foo.com"
        settings.SENDGRID_ALLOWED_SENDERS = ["example.com"]
        request = rf.post(reverse("sendgrid-webhook"), data=payload)
        response = webhook(request)
        assert response.status_code == 201
        assert Email.objects.count() == 0


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
        return rf.post(reverse("sendgrid-webhook"), data=payload)

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


class TestAllowList:
    @pytest.mark.parametrize(
        "sender,allowed_senders",
        [
            ("user@example.com", ["user@example.com"]),
            ("user@example.com", ["example.com"]),
            ("user@example.com", ["foo.io", "example.com"]),
        ],
    )
    def test_allowed_senders(self, sender, allowed_senders):
        assert email_is_allowed(sender, allowed_senders)

    @pytest.mark.parametrize(
        "sender,allowed_senders",
        [
            ("nope@example.com", ["user@example.com"]),
            ("user@example.com", ["user@foo.com"]),
            ("user@example.com", ["foo.com"]),
            ("user@example.com", ["foo.com", "bar.com"]),
        ],
    )
    def test_not_allowed_senders(self, sender, allowed_senders):
        assert not email_is_allowed(sender, allowed_senders)
