from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import OrganizationRegistrationForm

from .models import Organization
from django.shortcuts import get_object_or_404

from .utils import apply_plan_limits
from django.contrib.auth.decorators import login_required


def register_organization(request):

    if request.method == "POST":

        form = OrganizationRegistrationForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Organization registered successfully."
            )

            return redirect("organization_register")

    else:
        form = OrganizationRegistrationForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "organizations/register.html",
        context,
    )




@login_required
def organization_list(request):

    organizations = Organization.objects.all()

    context = {
        "organizations": organizations,
    }

    return render(
        request,
        "organizations/list.html",
        context,
    )




@login_required
def organization_detail(request, id=None):

    if id is None:
        organization = request.user.organization
    else:
        organization = get_object_or_404(
            Organization,
            id=id,
        )

    context = {
        "organization": organization,
    }

    return render(
        request,
        "organizations/organization_detail.html",
        context,
    )

@login_required
def organization_update(request, id):

    organization = get_object_or_404(
        Organization,
        id=id
    )

    if request.method == "POST":

        form = OrganizationRegistrationForm(
            request.POST,
            request.FILES,
            instance=organization,
        )

        if form.is_valid():

            organization = form.save()


            apply_plan_limits(
            organization
            )

            messages.success(
            request,
            "Organization updated successfully."
            )

            return redirect(
            "organization_detail",
            id=organization.id,
            )
    else:

        form = OrganizationRegistrationForm(
            instance=organization
        )


    context = {
        "form": form,
        "organization": organization,
    }


    return render(
        request,
        "organizations/update.html",
        context,
    )

@login_required
def organization_delete(request, id):

    organization = get_object_or_404(
        Organization,
        id=id
    )

    if request.method == "POST":

        organization.delete()

        messages.success(
            request,
            "Organization deleted successfully."
        )

        return redirect(
            "organization_list"
        )


    context = {
        "organization": organization,
    }


    return render(
        request,
        "organizations/delete.html",
        context,
    )

@login_required
def organization_toggle_status(request, id):

    organization = get_object_or_404(
        Organization,
        id=id
    )

    if organization.status == "ACTIVE":

        organization.status = "INACTIVE"
        message = "Organization deactivated successfully."

    else:

        organization.status = "ACTIVE"
        message = "Organization activated successfully."


    organization.save()


    messages.success(
        request,
        message
    )


    return redirect(
        "organization_detail",
        id=organization.id
    )