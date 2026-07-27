def get_current_organization(request):
    return getattr(
        request,
        "organization",
        None
    )