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
    create_invitation,
    accept_invitation,
    delete_user,
    invitation_list,
    resend_invitation,
    regenerate_invitation,
    resend_invitation_confirm,
    regenerate_invitation_confirm,
    view_invited_user,
    delete_invitation,
    
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
    "users/<int:user_id>/delete/",
    delete_user,
    name="delete_user"
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
    "invite-user/",
    create_invitation,
    name="create_invitation",
),
path(
    "accept-invitation/<uuid:token>/",
    accept_invitation,
    name="accept_invitation",
),
path(
    "invitations/",
    invitation_list,
    name="invitation_list",
),
path(
    "invitations/<int:id>/view/",
    view_invited_user,
    name="view_invited_user",
),
path(
    "invitations/<int:id>/resend/",
    resend_invitation,
    name="resend_invitation",
),

path(
    "invitations/<int:id>/resend/confirm/",
    resend_invitation_confirm,
    name="resend_invitation_confirm",
),

path(
    "invitations/<int:id>/regenerate/",
    regenerate_invitation,
    name="regenerate_invitation",
),

path(
    "invitations/<int:id>/regenerate/confirm/",
    regenerate_invitation_confirm,
    name="regenerate_invitation_confirm",
),
path(
    "invitations/<int:id>/delete/",
    delete_invitation,
    name="delete_invitation",
),

]