from django.contrib import admin
from django.urls import path, include

from core import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('organizations/', include('organizations.urls')),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')),   # ✅ IMPORTANT
    path('audit/', include('audit.urls')),   # ✅ IMPORTANT
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )