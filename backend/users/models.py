from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import validate_username


class CustomUser(AbstractUser):

    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        validators=[validate_username],
        help_text=_('Required. 4-20 characters. Letters and numbers only, start with letter.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    storage_path = models.CharField(max_length=100, blank=True, editable=False)

    is_admin = models.BooleanField(
        _('administrator'),
        default=False,
        help_text=_('Designates whether the user can manage other users and their files.')
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.username} ({self.full_name or self.email})"

    def save(self, *args, **kwargs):
        if not self.storage_path:
            if self.pk is None:
                super().save(*args, **kwargs)
                self.storage_path = f"user_{self.pk}"
                super().save(update_fields=['storage_path'])
                return

            self.storage_path = f"user_{self.pk}"

        super().save(*args, **kwargs)

    @property
    def storage_full_path(self):
        from django.conf import settings
        return settings.STORAGE_BASE / self.storage_path