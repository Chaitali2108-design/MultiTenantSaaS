from django.conf import settings
from django.db import models


class UserSetting(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_settings"
    )

    email_notifications = models.BooleanField(
        default=True
    )

    task_notifications = models.BooleanField(
        default=True
    )

    project_notifications = models.BooleanField(
        default=True
    )

    activity_notifications = models.BooleanField(
        default=True
    )

    compact_mode = models.BooleanField(
        default=False
    )

    show_completed_tasks = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "User Setting"
        verbose_name_plural = "User Settings"

    def __str__(self):
        return f"Settings - {self.user.username}"