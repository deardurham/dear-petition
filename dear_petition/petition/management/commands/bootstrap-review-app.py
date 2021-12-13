import os

from django.conf import settings
from django.contrib.auth import get_user_model  # pragma: no cover
from django.core.management.base import BaseCommand  # pragma: no cover


class Command(BaseCommand):  # pragma: no cover
    help = "Bootstrap Heroku review app"

    def handle(self, *args, **options):
        User = get_user_model()
        qatester_exists = User.objects.filter(email="qatester@example.com").exists()
        if os.getenv("IS_REVIEW", "False") != "True" or qatester_exists:
            self.stdout.write("**Not running bootstrap tasks**")
            return
        User.objects.create_superuser(username="qatester", email="qatester@example.com", password=settings.QATESTER_PASSWORD)
        self.stdout.write(self.style.SUCCESS("Successfully created qatester"))
