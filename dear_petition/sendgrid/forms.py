from django import forms

from .models import Email


class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["recipient"].required = False
        self.fields["sender"].required = False
        self.fields["from"] = self.fields["recipient"]
        self.fields["to"] = self.fields["sender"]

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["recipient"] = self.cleaned_data["to"]
        cleaned_data["sender"] = self.cleaned_data["from"]
        return cleaned_data

    class Meta:
        model = Email
        fields = ("subject", "recipient", "sender", "headers", "text", "html")
