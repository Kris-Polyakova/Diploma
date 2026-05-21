from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.utils import timezone
import os

from .models import UserFile
from .serializers import (
    UserFileListSerializer,
    UserFileUploadSerializer,
    UserFileUpdateSerializer
)


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin or request.user.is_superuser:
            return True
        return obj.owner == request.user


class FileListView(generics.ListAPIView):
    serializer_class = UserFileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = UserFile.objects.select_related('owner')

        user_id = self.request.query_params.get('user_id')

        if (user.is_admin or user.is_superuser) and user_id:
            print(f"INFO Админ {user.username} смотрит файлы пользователя ID={user_id}")
            return queryset.filter(owner_id=user_id)

        return queryset.filter(owner=user)


class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UserFileUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Файл успешно загружен"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserFile.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return UserFileUpdateSerializer
        return UserFileListSerializer

    def perform_destroy(self, instance):
        if os.path.exists(instance.full_disk_path):
            os.remove(instance.full_disk_path)
        print(f"INFO Файл '{instance.original_name}' удалён пользователем {self.request.user.username}")
        instance.delete()


class PublicDownloadView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        file_obj = get_object_or_404(UserFile, share_token=token)
        file_path = file_obj.full_disk_path

        if not os.path.exists(file_path):
            raise Http404("Файл не найден на сервере")

        file_obj.last_downloaded_at = timezone.now()
        file_obj.save(update_fields=['last_downloaded_at'])

        file_handle = open(file_path, 'rb')

        response = FileResponse(
            file_handle,
            as_attachment=True,
            filename=file_obj.original_name
        )

        response.file_to_close = file_handle

        return response