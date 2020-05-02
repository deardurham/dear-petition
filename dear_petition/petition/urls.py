from django.urls import path, include

from dear_petition.petition.views import (
    upload_report,
    view_record,
    create_petition,
    create_comment,
)

urlpatterns = [
    path("upload/", view=upload_report, name="upload-report"),
    path("view/ciprs/<int:pk>/", view=view_record, name="view-record"),
    path("api/", include("dear_petition.petition.api.urls", namespace="api")),
    path("create/<int:pk>/", view=create_petition, name="create-petition"),
    path("comments/<int:batch_id>", view=create_comment, name="create-comment"),
]
