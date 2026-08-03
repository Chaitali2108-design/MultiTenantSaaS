from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from projects.models import Project, Task, ActivityLog
from accounts.models import User, Role
from django.utils import timezone
from django.db.models import Q
@login_required
def dashboard(request):

    organization = request.user.organization
    search = request.GET.get("search", "")

    total_projects = Project.objects.filter(
        organization=organization
    ).count()

    completed_tasks = Task.objects.filter(
        organization=organization,
        status="done"
    ).count()

    pending_tasks = Task.objects.filter(
        organization=organization,
        status="todo"
    ).count()

    active_projects = Project.objects.filter(
        organization=organization
    ).count()

    overdue_tasks = 0

    for task in Task.objects.filter(
        organization=organization
    ):
        if task.is_overdue:
            overdue_tasks += 1

    # Recent Projects
    recent_projects = Project.objects.filter(
        organization=organization
    )

    if search:
        recent_projects = recent_projects.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    recent_projects = recent_projects.order_by("-created_at")[:5]

    # Recent Tasks
    recent_tasks = Task.objects.filter(
        organization=organization
    )

    if search:
        recent_tasks = recent_tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    recent_tasks = recent_tasks.order_by("-created_at")[:5]

    team_members = User.objects.filter(
        organization=organization
    ).count()

    progress_projects = Project.objects.filter(
        organization=organization
    ).order_by("-created_at")[:5]

    total_tasks = completed_tasks + pending_tasks + overdue_tasks

    if total_tasks > 0:
        completion_percentage = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        completion_percentage = 0

    recent_activities = ActivityLog.objects.filter(
        task__organization=organization
    ).order_by("-created_at")[:5]

    context = {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "recent_projects": recent_projects,
        "recent_tasks": recent_tasks,
        "team_members": team_members,
        "progress_projects": progress_projects,
        "completion_percentage": completion_percentage,
        "recent_activities": recent_activities,
        "now": timezone.now(),
        "search": search,
        "notification_count": recent_activities.count(),
    }

    return render(request, "dashboard.html", context)
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

