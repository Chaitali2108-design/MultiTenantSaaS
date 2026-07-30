from django.contrib.auth.decorators import login_required
from django.db.models import Count

from accounts.models import User
from organizations.models import Organization
from projects.models import Project, Task

from .models import AuditLog

from django.shortcuts import render


@login_required
def activity_report(request):

    if request.user.is_superuser:

        users = User.objects.all()

        organizations = Organization.objects.all()

        projects = Project.objects.all()

        tasks = Task.objects.all()

        logs = AuditLog.objects.all()


    else:

        organization = request.user.organization

        users = User.objects.filter(
            organization=organization
        )

        organizations = Organization.objects.filter(
            id=organization.id
        )

        projects = Project.objects.filter(
            organization=organization
        )

        tasks = Task.objects.filter(
            organization=organization
        )

        logs = AuditLog.objects.filter(
            organization=organization
        )


    context = {

        "total_users": users.count(),

        "total_organizations": organizations.count(),

        "total_projects": projects.count(),

        "total_tasks": tasks.count(),

        "total_logins": logs.filter(
            action="login"
        ).count(),

        "total_logouts": logs.filter(
            action="logout"
        ).count(),

        "recent_logs": logs.select_related(
            "user",
            "organization",
        ).order_by(
            "-created_at"
        )[:10],

        "action_summary": logs.values(
            "action"
        ).annotate(
            total=Count("id")
        ).order_by(
            "-total"
        ),
    }


    return render(
        request,
        "audit/activity_report.html",
        context,
    )