import logging

from django import forms

from django.contrib.auth import get_user_model


User = get_user_model()
logger = logging.getLogger(__name__)


class BookmarkletDataForm(forms.Form):
    user = forms.CharField()
    location = forms.CharField()
    source = forms.CharField()
    url = forms.CharField()

    def clean_user(self):
        try:
            return User.objects.get(username=self.cleaned_data["user"])
        except User.DoesNotExist:
            msg = "User does not exist"
            logger.exception(msg)
            raise forms.ValidationError(msg)
