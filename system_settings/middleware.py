from django.shortcuts import render
from django.urls import reverse

from .utils import get_setting


class MaintenanceModeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        maintenance_mode = get_setting(
            "maintenance_mode",
            "False"
        )


        if (
            maintenance_mode == "True"
            and not request.user.is_staff
            and request.path != reverse("admin:login")
        ):
            return render(
                request,
                "maintenance.html",
                status=503
            )


        response = self.get_response(request)

        return response