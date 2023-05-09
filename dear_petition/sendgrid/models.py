from django.db import models
from django.db.models import JSONField

from dear_petition.common.models import PrintableModelMixin


class Email(PrintableModelMixin, models.Model):
    """
    SendGrid Parse Email

    https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook#default-parameters
    """

    subject = models.CharField(max_length=4096, default="", blank=True) # It's possible to have no subject in email
    recipient = models.CharField(max_length=4096)  # aka "To"
    sender = models.CharField(max_length=4096)  # aka "From"
    headers = models.TextField()
    text = models.TextField(blank=True)
    html = models.TextField(blank=True)
    payload = JSONField()
    spam_score = models.FloatField(null=True, blank=True)
    attachment_count = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject[:20]} to {self.recipient}"


class Attachment(PrintableModelMixin, models.Model):
    """Email Attachment"""

    name = models.CharField(max_length=1024)
    content_id = models.CharField("Content ID", max_length=256, blank=True)
    type = models.CharField(max_length=256)
    file = models.FileField(upload_to="attachments/%Y/%m/%d/", max_length=1024)
    email = models.ForeignKey(
        Email, related_name="attachments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
