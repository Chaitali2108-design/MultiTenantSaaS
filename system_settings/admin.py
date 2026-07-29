from django.contrib import admin
from .models import SystemSetting


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):

    list_display = (
        "key",
        "category",
        "value",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "key",
        "value",
        "description",
    )

    ordering = (
        "category",
        "key",
    )