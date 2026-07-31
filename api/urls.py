from .views import (
    LoginAPIView,
    ProfileAPIView,
    LogoutAPIView,
)

from django.urls import path


urlpatterns = [

    path(
        "auth/login/",
        LoginAPIView.as_view(),
        name="api-login"
    ),

    path(
        "auth/profile/",
        ProfileAPIView.as_view(),
        name="api-profile"
    ),

    path(
        "auth/logout/",
        LogoutAPIView.as_view(),
        name="api-logout"
    ),

]