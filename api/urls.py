from .views import (
    LoginAPIView,
    ProfileAPIView,
    LogoutAPIView,
    OrganizationListCreateAPIView,
    OrganizationDetailAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    UserStatusAPIView,
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
    path(
    "organizations/",
    OrganizationListCreateAPIView.as_view(),
    name="organization-list-create",
),

path(
    "organizations/<int:pk>/",
    OrganizationDetailAPIView.as_view(),
    name="organization-detail",
),
path(
    "users/",
    UserListAPIView.as_view(),
    name="user-list",
),

path(
    "users/<int:pk>/",
    UserDetailAPIView.as_view(),
    name="user-detail",
),
path(
    "users/<int:pk>/update/",
    UserUpdateAPIView.as_view(),
    name="user-update",
),
path(
    "users/<int:pk>/status/",
    UserStatusAPIView.as_view(),
    name="user-status"
),

]