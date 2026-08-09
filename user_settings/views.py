from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserSettingForm
from .models import UserSetting


@login_required(login_url="/accounts/login/")
def settings_page(request):

    user = request.user

    settings, created = UserSetting.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        form = UserSettingForm(
            request.POST,
            instance=settings
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your preferences have been updated successfully."
            )

            return redirect("user_settings")

    else:

        form = UserSettingForm(
            instance=settings
        )

    return render(
        request,
        "user_settings/settings.html",
        {
            "form": form,
            "settings": settings,
            "organization": user.organization,
        }
    )