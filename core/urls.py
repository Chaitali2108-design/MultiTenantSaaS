from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


from core import settings
from django.conf.urls.static import static

def home_redirect(request):
    return redirect("login")

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", home_redirect, name="home"),

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
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )