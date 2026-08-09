from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from projects.models import Project, Task, ActivityLog
from accounts.models import User, Role
from django.utils import timezone
from django.db.models import Q
from audit.models import AuditLog
from projects.models import Team

from django.db.models import Count
from django.db.models.functions import TruncMonth

from datetime import date

@login_required
def dashboard(request):

    organization = request.user.organization
    search = request.GET.get("search", "")

    # =========================================================
    # BASIC COUNTS
    # =========================================================

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

    total_team_count = Team.objects.filter(
        project__organization=organization
    ).count()

    active_projects = Project.objects.filter(
        organization=organization,
        status__in=["todo", "progress"]
    ).count()


    # =========================================================
    # OVERDUE TASKS
    # =========================================================

    organization_tasks = Task.objects.filter(
        organization=organization
    )

    overdue_tasks = 0

    for task in organization_tasks:

        if task.is_overdue:
            overdue_tasks += 1


    # =========================================================
    # RECENT PROJECTS
    # =========================================================

    recent_projects = Project.objects.filter(
        organization=organization
    )

    if search:

        recent_projects = recent_projects.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    recent_projects = recent_projects.order_by(
        "-created_at"
    )[:5]


    # =========================================================
    # RECENT TASKS
    # =========================================================

    recent_tasks = Task.objects.filter(
        organization=organization
    )

    if search:

        recent_tasks = recent_tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    recent_tasks = recent_tasks.order_by(
        "-created_at"
    )[:5]


    # =========================================================
    # TEAM MEMBERS
    # =========================================================

    team_members = User.objects.filter(
        organization=organization
    ).count()


    # =========================================================
    # PROJECT PROGRESS
    # =========================================================

    progress_projects = Project.objects.filter(
        organization=organization
    ).order_by(
        "-created_at"
    )[:5]


    # =========================================================
    # COMPLETION PERCENTAGE
    # =========================================================

    total_tasks = (
        completed_tasks +
        pending_tasks +
        overdue_tasks
    )

    if total_tasks > 0:

        completion_percentage = int(
            (completed_tasks / total_tasks) * 100
        )

    else:

        completion_percentage = 0


    # =========================================================
    # RECENT ACTIVITIES
    # =========================================================

    recent_activities = ActivityLog.objects.filter(
        task__organization=organization
    ).order_by(
        "-created_at"
    )[:5]


    # =========================================================
    # PROJECT HISTORY
    # =========================================================

    project_history = AuditLog.objects.filter(
        organization=organization,
        project__isnull=False
    ).select_related(
        "user",
        "project"
    ).order_by(
        "-created_at"
    )[:10]


    # =========================================================
    # TASK HISTORY
    # =========================================================

    task_history = AuditLog.objects.filter(
        organization=organization,
        task__isnull=False
    ).select_related(
        "user",
        "task"
    ).order_by(
        "-created_at"
    )[:10]


    # =========================================================
    # CHART 1 — PROJECT STATUS
    # =========================================================

    project_status_data = Project.objects.filter(
        organization=organization
    ).values(
        "status"
    ).annotate(
        total=Count("id")
    )

    project_status = {
        "todo": 0,
        "progress": 0,
        "done": 0,
    }

    for item in project_status_data:

        status = item["status"]

        if status in project_status:
            project_status[status] = item["total"]


    # =========================================================
    # CHART 2 — TASK PRIORITY
    # =========================================================

    task_priority_data = Task.objects.filter(
        organization=organization
    ).values(
        "priority"
    ).annotate(
        total=Count("id")
    )

    task_priority = {
        "low": 0,
        "medium": 0,
        "high": 0,
    }

    for item in task_priority_data:

        priority = item["priority"]

        if priority in task_priority:
            task_priority[priority] = item["total"]


    # =========================================================
    # CHART 3 — MONTHLY TASKS
    # =========================================================

    # MONTHLY TASKS — JANUARY TO DECEMBER

    year = timezone.now().year

    monthly_task_labels = []
    monthly_task_values = []

    for month in range(1, 13):

        start_date = date(year, month, 1)

        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        count = Task.objects.filter(
            organization=organization,
            created_at__gte=start_date,
            created_at__lt=end_date
        ).count()

        monthly_task_labels.append(
            start_date.strftime("%b")
        )

        monthly_task_values.append(count)


    # =========================================================
    # CHART 4 — COMPLETED VS PENDING
    # =========================================================

    completed_count = Task.objects.filter(
        organization=organization,
        status="done"
    ).count()

    pending_count = Task.objects.filter(
        organization=organization
    ).exclude(
        status="done"
    ).count()

    progress_data = {
        "completed": completed_count,
        "pending": pending_count,
        "overdue":overdue_tasks,
    }


    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        # Dashboard counters
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,

        # Projects / Tasks
        "recent_projects": recent_projects,
        "recent_tasks": recent_tasks,
        "progress_projects": progress_projects,

        # Team
        "team_members": team_members,
        "total_team_count": total_team_count,

        # Progress
        "completion_percentage": completion_percentage,

        # History
        "project_history": project_history,
        "task_history": task_history,

        # Activities
        "notification_count": recent_activities.count(),

        # Search
        "search": search,

        # Time
        "now": timezone.now(),

        # =====================================================
        # CHART DATA
        # =====================================================

        "project_status": project_status,

        "task_priority": task_priority,

        "monthly_task_labels": monthly_task_labels,

        "monthly_task_values": monthly_task_values,

        "progress_data": progress_data,

    }


    return render(
        request,
        "dashboard.html",
        context
    )

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






def profile(request):
    return render(request, 'profile/profile.html')

@login_required(login_url="/accounts/login/")
def settings(request):
    return render(request, "user_settings/settings.html")

def organization(request):
    return render(request, "organizations/organization.html")

