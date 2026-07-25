from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('organizations/', include('organizations.urls')),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')),   # ✅ IMPORTANT
]