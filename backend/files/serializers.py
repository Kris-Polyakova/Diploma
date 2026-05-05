from rest_framework import serializers
from .models import UserFile
import os


class UserFileListSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = UserFile
        fields = [
            'id', 'original_name', 'size', 'comment',
            'uploaded_at', 'last_downloaded_at', 'download_url'
        ]
        read_only_fields = ['id', 'size', 'uploaded_at', 'last_downloaded_at', 'download_url']

    def get_download_url(self, obj):
        return obj.get_download_url()


class UserFileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = UserFile
        fields = ['file', 'original_name', 'comment']

    def validate_file(self, file):
        max_size = 500 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError(
                f"Файл слишком большой. Максимум 500 МБ."
            )

        allowed_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx',
            '.xls', '.xlsx', '.zip', '.rar', '.txt', '.mp4', '.mp3'
        }

        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Недопустимый тип файла: {ext}. Разрешены: {', '.join(allowed_extensions)}"
            )

        return file

    def create(self, validated_data):
        request = self.context['request']
        uploaded_file = validated_data.pop('file')
        original_name = validated_data.get('original_name') or uploaded_file.name

        ext = os.path.splitext(uploaded_file.name)[1].lower()
        unique_name = f"{os.urandom(8).hex()}{ext}"

        user_storage = request.user.storage_full_path
        user_storage.mkdir(parents=True, exist_ok=True)

        file_path_relative = request.user.storage_path

        full_path = user_storage / unique_name
        with open(full_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        user_file = UserFile.objects.create(
            owner=request.user,
            original_name=original_name,
            file_name=unique_name,
            file_path=file_path_relative,
            size=uploaded_file.size,
            comment=validated_data.get('comment', ''),
        )

        print(f"INFO Файл '{original_name}' загружен пользователем {request.user.username}")
        return user_file


class UserFileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ['original_name', 'comment']