from django.apps import AppConfig


class SystemSettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "system_settings"

    def ready(self):
        import system_settings.signals
