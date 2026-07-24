from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from .forms import OrganizationOwnerSignupForm

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


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