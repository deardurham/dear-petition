import json
import logging

from django import forms

from .models import Email


logger = logging.getLogger(__name__)


class EmailForm(forms.ModelForm):

    attachment_info = forms.CharField()
    # Field names to be re-keyed to match our Email model:
    # model_name -> sendgrid_name
    FIELD_MAP = {
        "recipient": "to",
        "sender": "from",
        "attachment_count": "attachments",
        "attachment_info": "attachment-info",
    }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        kwargs["data"] = self.map_sendgrid_keys_to_form(request.POST)
        kwargs["files"] = request.FILES
        super().__init__(*args, **kwargs)

    class Meta:
        model = Email
        fields = (
            "subject",
            "recipient",
            "sender",
            "headers",
            "text",
            "html",
            "spam_score",
            "attachment_count",
        )

    def map_sendgrid_keys_to_form(self, post_data):
        """Re-key POST data to match our form field names."""
        data = post_data.copy()
        for model_name, sendgrid_name in self.FIELD_MAP.items():
            try:
                sendgrid_value = data[sendgrid_name]
            except KeyError:
                logger.exception(f"{sendgrid_name} missing from POST data")
            data[model_name] = sendgrid_value
        return data

    def clean_attachment_info(self):
        try:
            return json.loads(self.cleaned_data["attachment_info"])
        except Exception:
            msg = "Failed to parse attachment_info JSON data"
            logger.exception(msg)
            raise forms.ValidationError(msg)

    def save(self):
        instance = super().save(commit=False)
        instance.payload = self.request.POST
        instance.save()
        logger.info(f'Email "{instance}" [id: {instance.id}] created')
        # Save any attachments in POST data
        for key, file_ in self.files.items():
            metadata = self.cleaned_data["attachment_info"][key]
            attachment = instance.attachments.create(
                name=metadata["name"],
                type=metadata["type"],
                content_id=metadata.get("content-id", ""),
                file=file_,
            )
            logger.info(f'Attachment {metadata["name"]} [id: {attachment.id}] created')
        return instance
