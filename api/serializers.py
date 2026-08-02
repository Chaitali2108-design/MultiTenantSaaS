from rest_framework import serializers
from accounts.models import User
from organizations.models import Organization
from accounts.models import Role
from accounts.models import Permission
from accounts.models import UserProfile




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



class PermissionSerializer(serializers.ModelSerializer):

    group = serializers.CharField(
        source="group.name",
        read_only=True,
    )

    class Meta:

        model = Permission

        fields = [
            "id",
            "name",
            "codename",
            "group",
        ]


class RoleSerializer(serializers.ModelSerializer):

    permission_count = serializers.SerializerMethodField()

    permissions = PermissionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = Role

        fields = [
            "id",
            "name",
            "description",
            "is_system",
            "is_editable",
            "permission_count",
            "permissions",      # ← Add this
            "created_at",
            "updated_at",
        ]

    def get_permission_count(self, obj):
        return obj.permissions.count()


class RoleCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Role

        fields = [
            "name",
            "description",
        ]


class RoleUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Role

        fields = [
            "name",
            "description",
        ]

class RolePermissionSerializer(serializers.Serializer):

    permissions = serializers.ListField(
        child=serializers.IntegerField()
    )

class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserProfile

        fields = [
            "profile_picture",
        ]