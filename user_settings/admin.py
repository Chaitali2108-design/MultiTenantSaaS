from django.contrib import admin

from .models import UserSetting


@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "email_notifications",
        "task_notifications",
        "project_notifications",
        "activity_notifications",
        "compact_mode",
        "show_completed_tasks",
        "updated_at",
    )

    list_filter = (
        "email_notifications",
        "task_notifications",
        "project_notifications",
        "activity_notifications",
        "compact_mode",
        "show_completed_tasks",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )