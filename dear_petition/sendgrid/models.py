from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Email(models.Model):
    """
    SendGrid Parse Email

    https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook#default-parameters
    """

    subject = models.CharField(max_length=4098)
    recipient = models.CharField(max_length=4098)  # aka "To"
    sender = models.TextField(max_length=4098)  # aka "From"
    headers = models.TextField()
    text = models.TextField()
    html = models.TextField(blank=True)
    payload = JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
