from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import SystemSetting


DEFAULT_SETTINGS = [
    {
        "key": "application_name",
        "value": "Secure Multi-Tenant SaaS",
        "category": "general",
        "description": "Application name displayed throughout the system.",
    },
    {
        "key": "support_email",
        "value": "support@example.com",
        "category": "general",
        "description": "Support contact email.",
    },
    {
        "key": "maintenance_mode",
        "value": "False",
        "category": "maintenance",
        "description": "Enable or disable maintenance mode.",
    },
    {
        "key": "max_upload_size_mb",
        "value": "5",
        "category": "security",
        "description": "Maximum upload size in MB.",
    },
]


@receiver(post_migrate)
def create_default_system_settings(sender, **kwargs):
    for setting in DEFAULT_SETTINGS:
        SystemSetting.objects.get_or_create(
            key=setting["key"],
            defaults=setting,
        )