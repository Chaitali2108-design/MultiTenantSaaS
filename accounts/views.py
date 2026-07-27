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





def login_view(request):

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
                "profile"
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



@login_required
def profile(request):

    

    return render(
        request,
        "accounts/profile.html"
    )

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect(
        "login"
    )


@login_required
@require_permission("view_user")
def role_list(request):

    roles = Role.objects.filter(
        organization=request.user.organization
    ).order_by("name")

    context = {
        "roles": roles,
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

            role.save()

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
@require_permission("view_user")
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