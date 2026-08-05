from django.shortcuts import render, redirect


def home(request):
    return render(
        request,
        "corepages/home.html",
    )


def features(request):

    return render(
        request,
        "corepages/features.html"
    )



from django.shortcuts import render

from organizations.models import Organization
from accounts.models import User
from projects.models import Project, Task


def organization_management(request):

    context = {
        "organization_count": Organization.objects.count(),
        "user_count": User.objects.count(),
        "project_count": Project.objects.count(),
        "task_count": Task.objects.count(),
    }

    return render(
        request,
        "corepages/organization_management.html",
        context,
    )


def user_management(request):
    return render(
        request,
        "corepages/user_management.html"
    )


def role_based_access(request):
    return render(
        request,
        "corepages/role_based_access.html"
    )


def project_management(request):
    return render(
        request,
        "corepages/project_management.html"
    )


def reports_analytics(request):
    return render(
        request,
        "corepages/reports_analytics.html"
    )