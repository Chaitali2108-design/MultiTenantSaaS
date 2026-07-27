from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Role
from .models import PermissionGroup, Permission


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "organization",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
        "organization",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Organization Details",
            {
                "fields": (
                    "organization",
                    "role",
                )
            }
        ),
    )




@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "organization",
        "is_system",
        "created_at",
    )

    list_filter = (
        "organization",
        "is_system",
    )

    search_fields = (
        "name",
        "organization__name",
    )
    filter_horizontal = (
        "permissions",
    )

@admin.register(PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "group",
        "codename",
        "created_at",
    )

    list_filter = (
        "group",
    )

    search_fields = (
        "name",
        "codename",
    )