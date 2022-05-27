import pytest

from faker import Faker

from django.urls import reverse

from dear_petition.sendgrid.forms import EmailForm

faker = Faker()


@pytest.fixture
def payload():
    return {
        "from": faker.email(),
        "to": faker.email(),
        "headers": "Received: by foo.sendgrid.net with SMTP id AAA Wed, 27 Jul 2016 20:53:06 +0000 (UTC)",
        "subject": faker.sentence(),
        "text": faker.paragraph(),
    }


@pytest.mark.django_db
class TestWebhookView:
    def test_get_not_allowed(self, client):
        response = client.get(reverse("sendgrid-webhook"))
        assert response.status_code == 405


class TestEmailForm:
    def test_form_payload(self, payload):
        form = EmailForm(payload)
        assert form.is_valid(), form.errors
        assert form.cleaned_data["recipient"] == payload["to"]
        assert form.cleaned_data["sender"] == payload["from"]
