from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "features/",
        views.features,
        name="features"
    ),

    path(
    "features/organization-management/",
    views.organization_management,
    name="organization_management"
),

path(
    "features/user-management/",
    views.user_management,
    name="user_management"
),

path(
    "features/role-based-access/",
    views.role_based_access,
    name="role_based_access"
),

path(
    "features/project-management/",
    views.project_management,
    name="project_management"
),

path(
    "features/reports-analytics/",
    views.reports_analytics,
    name="reports_analytics"
),
]