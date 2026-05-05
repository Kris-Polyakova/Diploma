from django.db import models
import uuid
from django.conf import settings
import os


class UserFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='files'
    )

    original_name = models.CharField(max_length=255)

    file_name = models.CharField(max_length=255)

    file_path = models.CharField(max_length=500)

    size = models.PositiveBigIntegerField()

    comment = models.TextField(blank=True, default='')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    last_downloaded_at = models.DateTimeField(null=True, blank=True)

    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.original_name} ({self.owner.username})"

    @property
    def full_disk_path(self):
        return settings.STORAGE_BASE / self.file_path / self.file_name

    def get_download_url(self):
        return f"/api/download/{self.share_token}/"