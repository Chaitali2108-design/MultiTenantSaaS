from .models import AuditLog
from .middleware import get_current_request


def get_client_ip(request):

    x_forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if x_forwarded_for:

        return x_forwarded_for.split(",")[0]

    return request.META.get(
        "REMOTE_ADDR"
    )


def create_audit_log(
    action,
    model_name,
    description,
    object_id=None,
):

    request = get_current_request()

    user = None
    organization = None
    ip_address = None


    if request:

        ip_address = get_client_ip(request)


        if request.user.is_authenticated:

            user = request.user

            organization = getattr(
                request.user,
                "organization",
                None
            )


    AuditLog.objects.create(

        user=user,

        organization=organization,

        action=action,

        model_name=model_name,

        object_id=object_id or "",

        description=description,

        ip_address=ip_address,

    )