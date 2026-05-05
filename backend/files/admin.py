from django.contrib import admin
from .models import UserFile


@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):

    list_display = ('original_name', 'owner', 'size', 'uploaded_at', 'last_downloaded_at')
    list_filter = ('owner', 'uploaded_at')
    search_fields = ('original_name', 'comment', 'owner__username')

    readonly_fields = ('id', 'share_token', 'file_path', 'file_name', 'size', 'uploaded_at')

    fieldsets = (
        (None, {
            'fields': ('owner', 'original_name', 'comment')
        }),
        ('Техническая информация', {
            'fields': ('file_path', 'file_name', 'size', 'share_token', 'uploaded_at', 'last_downloaded_at'),
            'classes': ('collapse',)
        }),
    )