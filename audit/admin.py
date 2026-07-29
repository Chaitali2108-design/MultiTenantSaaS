from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "organization",
        "action",
        "model_name",
        "object_id",
        "ip_address",
        "created_at",
    )


    list_filter = (
        "action",
        "organization",
        "created_at",
    )


    search_fields = (
        "user__username",
        "model_name",
        "description",
        "object_id",
    )


    readonly_fields = (
        "user",
        "organization",
        "action",
        "model_name",
        "object_id",
        "description",
        "ip_address",
        "created_at",
    )


    ordering = (
        "-created_at",
    )


    def has_change_permission(
        self,
        request,
        obj=None
    ):

        return False


    def has_delete_permission(
        self,
        request,
        obj=None
    ):

        return False