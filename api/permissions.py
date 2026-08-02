def has_admin_permission(user):

    if not user.is_authenticated:
        return False


    if not user.role:
        return False


    return user.role.name in [
        "Owner",
        "Admin",
    ]