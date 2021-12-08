from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, ForeignKey
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail


from . import constants as uc


class User(AbstractUser):

    name = CharField(_("Name of User"), blank=True, max_length=uc.NAME_MAX_LENGTH)
    last_generated_petition_time = DateField(null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def send_email(self, subject, message, send_anyway=False):
        if settings.ENVIRONMENT == "PRODUCTION" or send_anyway:
            send_mail(subject, message, uc.FROM_EMAIL_ADDRESS, [self.email])
