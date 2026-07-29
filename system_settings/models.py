from django.db import models


class SystemSetting(models.Model):

    SETTING_TYPES = [
        ("general", "General"),
        ("security", "Security"),
        ("email", "Email"),
        ("maintenance", "Maintenance"),
    ]

    key = models.CharField(
        max_length=100,
        unique=True,
    )

    value = models.TextField(
        blank=True,
        null=True,
    )

    category = models.CharField(
        max_length=20,
        choices=SETTING_TYPES,
        default="general",
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["category", "key"]
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return self.key