from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from .models import (
    User,
    Role,
    PermissionGroup,
    Permission,
)

class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        # Initially hide all roles
        self.fields["role"].queryset = Role.objects.none()


        # When editing existing user
        if self.instance.pk:

            if self.instance.organization:

                self.fields["role"].queryset = Role.objects.filter(
                    organization=self.instance.organization
                )


        # When creating new user
        elif "organization" in self.data:

            try:

                organization_id = int(
                    self.data.get("organization")
                )


                self.fields["role"].queryset = Role.objects.filter(
                    organization_id=organization_id
                )


            except (ValueError, TypeError):

                pass

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    form = UserAdminForm

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

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Organization Details",
            {
                "fields": (
                    "organization",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                    "organization",
                    "role",
                    "is_active",
                    "is_staff",
                ),
            },
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

from .models import UserInvitation


@admin.register(UserInvitation)
class UserInvitationAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "organization",
        "role",
        "is_accepted",
        "created_at",
    )
    readonly_fields = (
    "token",
)


    list_filter = (
        "organization",
        "is_accepted",
    )


    search_fields = (
        "email",
    )