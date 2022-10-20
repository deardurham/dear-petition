import pytest
from unittest import mock

from dear_petition.sendgrid.actions import notify_sendgrid_listeners

from .factories import EmailFactory


def my_listener(email_id):
    raise Exception("Hi")


@pytest.mark.django_db
def test_no_listeners():
    """No errors should raise if no listeners exist"""
    email = EmailFactory()
    notify_sendgrid_listeners(email.id)


@pytest.mark.django_db
def test_listener_listeners(settings):
    """"""
    settings.SENDGRID_WEBHOOK_LISTENERS = [
        "dear_petition.sendgrid.tests.test_notify.my_listener"
    ]
    email = EmailFactory()
    with mock.patch("dear_petition.sendgrid.tests.test_notify.my_listener") as mock_:
        notify_sendgrid_listeners(email.id)
        assert mock_.assert_called_once
