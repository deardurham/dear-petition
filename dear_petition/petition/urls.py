from django.urls import path

from dear_petition.petition.views import upload_report, view_record, create_petition

urlpatterns = [
    path("upload/", view=upload_report, name="upload-report"),
    path("view/ciprs/<int:pk>/", view=view_record, name="view-record"),
    path("create/<int:pk>/", view=create_petition, name="create-petition"),
]
