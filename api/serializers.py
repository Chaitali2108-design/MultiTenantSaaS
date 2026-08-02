from rest_framework import serializers
from accounts.models import User
from organizations.models import Organization


class UserSerializer(serializers.ModelSerializer):

    organization = serializers.CharField(
        source="organization.name",
        read_only=True
    )

    role = serializers.CharField(
        source="role.name",
        read_only=True
    )


    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "organization",
            "role",
            "is_active",
            "created_at",
        ]



class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Organization

        fields = [
            "id",
            "name",
            "domain",
            "logo",
            "contact_email",
            "contact_phone",
            "plan",
            "status",
            "max_users",
            "max_projects",
            "storage_limit_gb",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "max_users",
            "max_projects",
            "storage_limit_gb",
            "created_at",
            "updated_at",
        ]




class UserManagementSerializer(serializers.ModelSerializer):

    organization = serializers.CharField(
        source="organization.name",
        read_only=True
    )

    role = serializers.CharField(
        source="role.name",
        read_only=True
    )

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "organization",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "organization",
            "created_at",
            "updated_at",
        ]

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "is_active",
        ]


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "is_active",
        ]