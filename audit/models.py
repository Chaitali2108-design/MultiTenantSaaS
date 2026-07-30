from django.db import models
from django.conf import settings
from organizations.models import Organization


class AuditLog(models.Model):

    ACTION_TYPES = [

        ("create", "Create"),

        ("update", "Update"),

        ("delete", "Delete"),

        ("login", "Login"),

        ("logout", "Logout"),

        ("permission", "Permission Change"),

    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )


    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


    action = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
    )


    model_name = models.CharField(
        max_length=100,
    )


    object_id = models.CharField(
        max_length=100,
        blank=True,
    )


    description = models.TextField(
        blank=True,
    )


    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    class Meta:

        ordering = [
            "-created_at"
        ]


    def __str__(self):

        return f"{self.user} - {self.action} - {self.model_name}"