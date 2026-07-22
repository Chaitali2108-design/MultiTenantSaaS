from django.urls import path
from .views import (
    register_organization,
    organization_list,
    organization_detail,
    organization_update,
    organization_delete,
    organization_toggle_status,
)


urlpatterns = [
    path(
        "register/",
        register_organization,
        name="organization_register",
    ),

    path(
        "list/",
        organization_list,
        name="organization_list",
    ),

    path(
    "detail/<int:id>/",
    organization_detail,
    name="organization_detail",
    ),

    path(
    "update/<int:id>/",
    organization_update,
    name="organization_update",
    ),

    path(
    "delete/<int:id>/",
    organization_delete,
    name="organization_delete",
    ),

    path(
    "status/<int:id>/",
    organization_toggle_status,
    name="organization_toggle_status",
    ),

]