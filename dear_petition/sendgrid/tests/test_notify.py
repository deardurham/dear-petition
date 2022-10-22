from unittest import mock

from dear_petition.sendgrid.actions import notify_sendgrid_listeners


def my_listener(email_id):
    raise Exception("Hi")


def test_no_listeners(settings):
    """No-op if no listeners are defined"""
    settings.SENDGRID_WEBHOOK_LISTENERS = []
    notify_sendgrid_listeners(1)


def test_defined_listener(settings):
    """Defined listener should be called when notify_sendgrid_listeners is triggered"""
    settings.SENDGRID_WEBHOOK_LISTENERS = [
        "dear_petition.sendgrid.tests.test_notify.my_listener"
    ]
    with mock.patch("dear_petition.sendgrid.tests.test_notify.my_listener") as mock_:
        notify_sendgrid_listeners(1)
        assert mock_.assert_called_once
