from django.urls import path
from django.contrib.auth import views as auth_views


from .views import (
    signup,
    login_view,
    profile,
    logout_view,
    role_list,
    role_create,
    role_update,
    role_delete,
    user_list,
    assign_user_role,
    update_profile,
    upload_profile_picture,
    account_settings,
    logout_all_sessions,
    organization_users,
    create_invitation,
    accept_invitation,
    
)




urlpatterns = [

    path(
        "signup/",
        signup,
        name="signup",
    ),

    path(
        "login/",
        login_view,
        name="login",
    ),

    path(
        "profile/",
        profile,
        name="profile",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),


    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
    "change-password/",
    auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html"
    ),
    name="password_change",
),

path(
    "change-password/done/",
    auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"
    ),
    name="password_change_done",
),

path(
    "roles/",
    role_list,
    name="role_list",
),
path(
    "roles/create/",
    role_create,
    name="role_create",
),
path(
    "roles/<int:pk>/edit/",
     role_update,
    name="role_update",
),

path(
    "roles/<int:pk>/delete/",
    role_delete,
    name="role_delete",
),

path(
    "users/",
    user_list,
    name="user_list",
),

path(
    "users/<int:pk>/assign-role/",
    assign_user_role,
    name="assign_user_role",
),

path(
    "profile/edit/",
    update_profile,
    name="update_profile",
),

path(
    "profile/picture/",
    upload_profile_picture,
    name="upload_profile_picture",
),

path(
    "settings/",
    account_settings,
    name="account_settings",
),
path(
    "logout-all/",
    logout_all_sessions,
    name="logout_all_sessions",
),

path(
    "organization-users/",
     organization_users,
    name="organization_users",
),
path(
    "invite-user/",
    create_invitation,
    name="create_invitation",
),
path(
    "accept-invitation/<uuid:token>/",
    accept_invitation,
    name="accept_invitation",
),




]
