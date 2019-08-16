from django.urls import path

from dear_petition.petition.views import upload_report, view_record

urlpatterns = [
    path("upload/", view=upload_report, name="upload-report"),
    path("view/<int:pk>/", view=view_record, name="view-record"),
]
