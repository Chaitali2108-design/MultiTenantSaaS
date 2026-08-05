from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from .forms import OrganizationOwnerSignupForm

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Role
from .forms import RoleForm
from .forms import UserRoleForm
from .models import User
from django.shortcuts import get_object_or_404
from .permissions import require_permission
from .forms import UserProfileForm
from .forms import ProfilePictureForm
from .models import UserProfile
from .forms import AccountSettingsForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from .forms import AcceptInvitationForm
from .models import UserInvitation
from .utils import assign_default_permissions
from django.db.models import Case, When, Value, IntegerField
from .utils import send_invitation_email


User = get_user_model()


def signup(request):

    if request.method == "POST":

        form = OrganizationOwnerSignupForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            with transaction.atomic():

                form.save()

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect("login")

    else:

        form = OrganizationOwnerSignupForm()


    context = {
        "form": form,
    }


    return render(
        request,
        "accounts/signup.html",
        context,
    )




@never_cache
def login_view(request):

    messages.get_messages(request).used = True

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )


        user = authenticate(
            request,
            username=username,
            password=password,
        )


        if user is not None:

            login(
                request,
                user
            )

            

            return redirect(
                "dashboard"
            )


        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            


    return render(
        request,
        "accounts/login.html"
    )


@never_cache
@login_required
def profile(request):

    

    return render(
        request,
        "profile.html"
    )

def logout_view(request):


    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    messages.get_messages(request).used = True

    return redirect(
        "login"
    )


@login_required
def role_list(request):

    roles = Role.objects.filter(
        organization=request.user.organization
    ).annotate(
        role_order=Case(
            When(name="Owner", then=Value(1)),
            When(name="Admin", then=Value(2)),
            When(name="Manager", then=Value(3)),
            When(name="Member", then=Value(4)),
            When(name="Viewer", then=Value(5)),
            default=Value(6),
            output_field=IntegerField(),
        )
    ).order_by(
    "role_order",
    "name"
    )

    owner = User.objects.filter(
        organization=request.user.organization,
        role__name="Owner"
    ).first()

    context = {
        "roles": roles,
        "owner": owner,
    }

    return render(
        request,
        "accounts/roles/role_list.html",
        context,
    )





@login_required
def role_create(request):

    if request.method == "POST":

        form = RoleForm(request.POST)

        if form.is_valid():

            role = form.save(commit=False)

            role.organization = request.user.organization
            role.is_system = False
            role.is_editable = True

            role.save()

            # Copy Member permissions
            assign_default_permissions(role)

            messages.success(
                request,
                "Role created successfully.",
            )

            return redirect("role_list")

    else:
        form = RoleForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/roles/role_form.html",
        context,
    )

@login_required
def role_update(request, pk):

    role = get_object_or_404(
        Role,
        pk=pk,
        organization=request.user.organization,
    )

    if role.is_system:
        messages.error(
            request,
            "System roles cannot be edited.",
        )
        return redirect("role_list")

    if request.method == "POST":

        form = RoleForm(
            request.POST,
            instance=role,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Role updated successfully.",
            )

            return redirect("role_list")

    else:

        form = RoleForm(instance=role)

    return render(
        request,
        "accounts/roles/role_form.html",
        {
            "form": form,
        },
    )

@login_required
def role_delete(request, pk):

    role = get_object_or_404(
        Role,
        pk=pk,
        organization=request.user.organization,
    )

    if role.is_system:

        messages.error(
            request,
            "System roles cannot be deleted.",
        )

        return redirect("role_list")


    if request.method == "POST":

        role.delete()

        messages.success(
            request,
            "Role deleted successfully.",
        )

        return redirect("role_list")


    return render(
        request,
        "accounts/roles/role_confirm_delete.html",
        {
            "role": role,
        },
    )

@login_required
def user_list(request):

    users = User.objects.filter(
        organization=request.user.organization
    )

    return render(
        request,
        "accounts/users/user_list.html",
        {
            "users": users,
        },
    )

@login_required
def assign_user_role(request, pk):

    user = get_object_or_404(
        User,
        pk=pk,
        organization=request.user.organization,
    )


    if user == request.user:
        return redirect("user_list")


    if request.method == "POST":

        form = UserRoleForm(
            request.POST,
            instance=user,
            organization=request.user.organization,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "user_list"
            )

    else:

        form = UserRoleForm(
            instance=user,
            organization=request.user.organization,
        )


    return render(
        request,
        "accounts/users/assign_role.html",
        {
            "form": form,
            "user": user,
        },
    )



@login_required
def delete_user(request, user_id):

    if request.method == "POST":

        user = get_object_or_404(
            User,
            id=user_id,
            organization=request.user.organization
        )

        if user != request.user:
            user.delete()

    return redirect("user_list")

@login_required
def update_profile(request):

    if request.method == "POST":

        form = UserProfileForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect(
                "profile"
            )

    else:

        form = UserProfileForm(
            instance=request.user,
        )

    return render(
        request,
        "accounts/profile_update.html",
        {
            "form": form,
        },
    )

@login_required
def upload_profile_picture(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfilePictureForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile picture updated successfully."
            )

            return redirect(
                "profile"
            )

    else:

        form = ProfilePictureForm(
            instance=profile
        )


    return render(
        request,
        "accounts/upload_profile_picture.html",
        {
            "form": form,
        },
    )

@login_required
def account_settings(request):

    profile = request.user.profile


    if request.method == "POST":

        form = AccountSettingsForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account settings updated successfully."
            )

            return redirect(
                "profile"
            )

    else:

        form = AccountSettingsForm(
            instance=profile
        )


    return render(
        request,
        "accounts/account_settings.html",
        {
            "form": form,
        },
    )



@login_required
def logout_all_sessions(request):

    user_id = request.user.id

    sessions = Session.objects.filter(
        expire_date__gte=timezone.now()
    )


    for session in sessions:

        data = session.get_decoded()

        if data.get("_auth_user_id") == str(user_id):

            session.delete()


    logout(request)

    return redirect("login")




from django.contrib import messages
from django.shortcuts import redirect

from .forms import UserInvitationForm
from .models import UserInvitation


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from datetime import timedelta
from django.utils import timezone

@login_required
def create_invitation(request):

    if request.method == "POST":

        form = UserInvitationForm(
            request.POST,
            organization=request.user.organization
        )


        if form.is_valid():

            invitation = form.save(
                commit=False
            )


            invitation.organization = (
                request.user.organization
            )


            invitation.save()


            from django.urls import reverse

            invitation_url = request.build_absolute_uri(
                reverse(
                    "accept_invitation",
                kwargs={
                    "token": invitation.token
                }
            )
        )

            return render(
                request,
                "accounts/invitation_success.html",
                {
                    "invitation": invitation,
                    "invitation_url": invitation_url,
                },
            )


    else:

        form = UserInvitationForm(
            organization=request.user.organization
        )


    return render(
        request,
        "accounts/create_invitation.html",
        {
            "form": form
        }
    )

def accept_invitation(request, token):

    invitation = get_object_or_404(
        UserInvitation,
        token=token,
    )

    if invitation.is_accepted:

        messages.error(
            request,
            "This invitation has already been used."
        )

        return redirect("login")

    if (
        invitation.expires_at
        and invitation.expires_at < timezone.now()
    ):

        messages.error(
            request,
            "This invitation has expired."
        )

        return redirect("login")

    if request.method == "POST":

        form = AcceptInvitationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.email = invitation.email

            user.organization = invitation.organization

            user.role = invitation.role

            user.set_password(
                form.cleaned_data["password1"]
            )

            user.save()

            invitation.user = user

            invitation.is_accepted = True

            invitation.accepted_at = timezone.now()

            invitation.save()

            messages.success(
                request,
                "Account created successfully. Please log in."
            )

            return redirect("login")

    else:

        form = AcceptInvitationForm()

    return render(
        request,
        "accounts/accept_invitation.html",
        {
            "form": form,
            "invitation": invitation,
        },
    )


@login_required
def invitation_list(request):

    invitations = UserInvitation.objects.filter(
        organization=request.user.organization
    ).order_by(
        "-created_at"
    )

    context = {
    "total_invitations": invitations.count(),
    "invitations": invitations,
}


    return render(
        request,
        "accounts/invitation_list.html",
        context,
    )

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

@login_required
def view_invited_user(request, id):

    invitation = get_object_or_404(
        UserInvitation,
        id=id,
        organization=request.user.organization,
    )

    print("INVITATION:", invitation)
    print("ACCEPTED:", invitation.is_accepted)
    print("CONNECTED USER:", invitation.user)

    if not invitation.is_accepted or invitation.user is None:

        messages.error(
            request,
            "This invitation has not been accepted yet."
        )

        return redirect("invitation_list")

    return render(
        request,
        "accounts/invited_user_detail.html",
        {
            "invitation": invitation,
            "user": invitation.user,
        },
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

@login_required
def resend_invitation(request, id):

    invitation = get_object_or_404(
        UserInvitation,
        id=id,
        organization=request.user.organization,
    )

    invitation_url = request.build_absolute_uri(
        reverse(
            "accept_invitation",
            kwargs={
                "token": invitation.token
            }
        )
    )

    return render(
        request,
        "accounts/invitation_detail.html",
        {
            "invitation": invitation,
            "invitation_url": invitation_url,
            "page_title": "Resend Invitation",
            "button_text": "Resend Invitation",
            "button_url": reverse(
                "resend_invitation_confirm",
                args=[invitation.id]
            ),
        },
    )

@login_required
def regenerate_invitation(request, id):

    invitation = get_object_or_404(
        UserInvitation,
        id=id,
        organization=request.user.organization,
    )

    invitation_url = request.build_absolute_uri(
        reverse(
            "accept_invitation",
            kwargs={
                "token": invitation.token
            }
        )
    )

    return render(
        request,
        "accounts/invitation_detail.html",
        {
            "invitation": invitation,
            "invitation_url": invitation_url,
            "page_title": "Regenerate Invitation",
            "button_text": "Generate New Link",
            "button_url": reverse(
                "regenerate_invitation_confirm",
                args=[invitation.id]
            ),
        },
    )

from django.contrib import messages

@login_required
def resend_invitation_confirm(request, id):

    invitation = get_object_or_404(
        UserInvitation,
        id=id,
        organization=request.user.organization,
    )

    messages.success(
        request,
        "Invitation is ready to share again."
    )

    return redirect(
        "resend_invitation",
        id=invitation.id
    )

import uuid

@login_required
def regenerate_invitation_confirm(request, id):

    invitation = get_object_or_404(
        UserInvitation,
        id=id,
        organization=request.user.organization,
    )

    invitation.token = uuid.uuid4()
    invitation.save()

    messages.success(
        request,
        "Invitation link regenerated successfully."
    )

    return redirect(
        "regenerate_invitation",
        id=invitation.id
    )

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def delete_invitation(request, id):

    invitation = get_object_or_404(
        UserInvitation,
        id=id,
        organization=request.user.organization,
    )


    if invitation.is_accepted:

        messages.error(
            request,
            "Accepted invitations cannot be deleted."
        )

        return redirect("invitation_list")


    if request.method == "POST":

        invitation.delete()

        messages.success(
            request,
            "Invitation deleted successfully."
        )

        return redirect("invitation_list")


    return render(
        request,
        "accounts/delete_invitation_confirm.html",
        {
            "invitation": invitation,
        },
    )