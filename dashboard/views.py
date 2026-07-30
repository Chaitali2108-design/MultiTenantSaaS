from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def project_list(request):
    return render(request, 'projects/project_list.html')

def task_list(request):
    return render(request, 'tasks/task_list.html')

def kanban(request):
    return render(request, 'tasks/kanban.html')

def tasks(request):
    return render(request, "tasks/tasks.html")

def reports(request):
    return render(request, "reports/reports.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import User, Role


@login_required
def team_members(request):

    users = User.objects.filter(
        organization=request.user.organization
    )

    roles = Role.objects.filter(
        organization=request.user.organization
    )

    context = {
        "users": users,
        "roles": roles,
        "admin_count": users.filter(role__name="Admin").count(),
        "manager_count": users.filter(role__name="Manager").count(),
        "member_count": users.filter(role__name="Member").count(),
    }

    return render(
        request,
        "team_members/team_members.html",
        context,
    )

def profile(request):
    return render(request, 'profile/profile.html')

def settings(request):
    return render(request, 'settings/settings.html')

def organization(request):
    return render(request, "organizations/organization.html")

