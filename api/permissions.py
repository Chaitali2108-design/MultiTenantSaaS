def has_admin_permission(user):

    if not user.is_authenticated:
        return False


    if not user.role:
        return False


    return user.role.name in [
        "Owner",
        "Admin",
    ]

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        if not request.user.is_authenticated:
            return False

        if not request.user.role:
            return False

        return (
            request.user.role.name.lower()
            == "owner"
        )



class IsAdminOrOwner(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        if not request.user.is_authenticated:
            return False

        if not request.user.role:
            return False

        return request.user.role.name.lower() in [
            "owner",
            "admin",
        ]


class HasOrganization(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and request.user.organization
            is not None
        )