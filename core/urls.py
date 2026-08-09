from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("corepages.urls")),

    path(
        "organizations/",
        include("organizations.urls"),
    ),

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    path(
        "projects/",
        include("projects.urls"),
    ),

    path(
        "audit/",
        include("audit.urls"),
    ),

    path(
        "dashboard/",
        include("dashboard.urls"),
    ),

    path(
        "api/",
        include("api.urls"),
    ),



path(
    "reports/",
    include("reports.urls"),
),

path(
        "settings/",
        include("user_settings.urls")
    ),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )