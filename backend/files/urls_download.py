from django.urls import path
from .views import PublicDownloadView

urlpatterns = [
    path('<uuid:token>/', PublicDownloadView.as_view(), name='public-download'),
]