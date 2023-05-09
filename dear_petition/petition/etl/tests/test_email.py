import pytest

from dear_petition.petition.etl.email import (
    extract_username_and_label,
    sendgrid_webhook_listener,
)
from dear_petition.petition.models import CIPRSRecord
from dear_petition.petition.tests.factories import record_data
from dear_petition.sendgrid.tests.factories import AttachmentFactory, EmailFactory
from dear_petition.users.tests.factories import UserFactory


@pytest.mark.parametrize(
    "attr,username,label",
    [
        ("user@example.com", "user", ""),
        ("user+mylabel@example.com", "user", "mylabel"),
        ("first.last@example.com", "first.last", ""),
        ("first.last+mylabel@example.com", "first.last", "mylabel"),
        ("first.last+Test_Client_name@example.com", "first.last", "Test Client name"),
    ],
)
def test_extract(attr, username, label):
    extracted_username, extracted_label = extract_username_and_label(attr)
    assert extracted_username == username
    assert extracted_label == label


@pytest.mark.django_db
class TestWebhookListener:
    def test_email_linked_to_batch(self):
        """Listener should associate users by username"""
        UserFactory(username="gina")
        email = EmailFactory(recipient="gina@deardurham.org")
        batch = sendgrid_webhook_listener(email_id=email.id)
        assert batch.emails.filter(id=email.id).exists()

    def test_email_not_linked_to_batch(self):
        """Listener should not match to other users"""
        UserFactory(username="gina")
        email = EmailFactory(recipient="jessica@deardurham.org")
        batch = sendgrid_webhook_listener(email_id=email.id)
        assert not batch

    def test_batch_file_linked(self, mock_ciprs_reader):
        """Webhook email attachments should become BachFiles"""
        UserFactory(username="gina")
        email = EmailFactory(recipient="gina@deardurham.org")
        attachment = AttachmentFactory(email=email)
        batch = sendgrid_webhook_listener(email_id=email.id)
        assert batch.files.filter(file=attachment.file).exists()

    def test_ciprs_record_batch_file_linked(self, mock_ciprs_reader, fake_pdf):
        """CIPRS records should link back to their source BatchFile"""
        mock_ciprs_reader.return_value = [record_data(1)]
        UserFactory(username="gina")
        email = EmailFactory(recipient="gina@deardurham.org")
        AttachmentFactory(email=email, file=fake_pdf)
        batch = sendgrid_webhook_listener(email_id=email.id)
        assert CIPRSRecord.objects.filter(batch_file__batch=batch).exists()
