from django.core.exceptions import PermissionDenied


def has_permission(user, codename):
    """
    Check whether the user's role contains
    the specified permission codename.
    """

    if not user.is_authenticated:
        return False

    if not user.role:
        return False

    return user.role.permissions.filter(
        codename=codename
    ).exists()


def require_permission(codename):
    """
    Decorator for protecting views.
    """

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if not has_permission(
                request.user,
                codename,
            ):
                raise PermissionDenied

            return view_func(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator