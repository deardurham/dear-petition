from django.urls import path

from dear_petition.petition.views import (
    upload_report,
)

urlpatterns = [
    path("upload/", view=upload_report, name="upload-report"),
]
