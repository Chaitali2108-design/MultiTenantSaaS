from django.shortcuts import render, redirect
from .models import ContactMessage
from organizations.models import Organization
from accounts.models import User
from projects.models import Project, Task

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

def solutions(request):
    return render(request, "corepages/solutions.html")


def enterprise_solution(request):
    return render(request, "corepages/enterprise.html")


def startup_solution(request):
    return render(request, "corepages/startups.html")


def education_solution(request):
    return render(request, "corepages/education.html")

def pricing(request):
    return render(request, "corepages/pricing.html")

def about(request):
    return render(request, "corepages/about.html")



from django.contrib import messages



def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )

        messages.success(
            request,
            "Your message has been sent successfully."
        )

        return redirect("contact")

    return render(request, "corepages/contact.html")