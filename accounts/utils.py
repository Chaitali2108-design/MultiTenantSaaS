from .models import Role


def assign_default_permissions(role):
    """
    Assign Member permissions to newly created custom roles.
    """

    try:
        member_role = Role.objects.get(
            organization=role.organization,
            name="Member",
        )

        role.permissions.set(
            member_role.permissions.all()
        )

    except Role.DoesNotExist:
        pass