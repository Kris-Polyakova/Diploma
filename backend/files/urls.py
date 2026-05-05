from django.urls import path
from .views import (
    FileListView, FileUploadView, FileDetailView, PublicDownloadView
)

urlpatterns = [
    path('', FileListView.as_view(), name='file-list'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('<uuid:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('download/<uuid:token>/', PublicDownloadView.as_view(), name='public-download'),
]