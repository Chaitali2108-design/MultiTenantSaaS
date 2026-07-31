from rest_framework import serializers
from accounts.models import User


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