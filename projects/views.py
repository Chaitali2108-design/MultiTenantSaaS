from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import csv
from datetime import datetime, date

from accounts.models import User

from .models import Project, Task, ActivityLog, Notification, ProjectMember, Team



def create_notification(user, message):
    if user:
        Notification.objects.create(
            user=user,
            message=message
        )

# ================= REMINDER CHECK =================

def check_reminders(request):

    now = timezone.now()

    tasks = Task.objects.filter(
        reminder_date__lte=now,
        reminder_sent=False
    )


    for task in tasks:

        if task.priority == "high":

            message = f"🚨 HIGH PRIORITY Reminder: {task.title}"

        elif task.priority == "medium":

            message = f"⚠️ Reminder: {task.title}"

        else:

            message = f"🔔 Reminder: {task.title}"


        # Save notification in database
        if task.assigned_to:

            create_notification(
                task.assigned_to,
                message
            )


            # Optional UI message
            if task.assigned_to == request.user:
                messages.warning(
                    request,
                    message
                )


        task.reminder_sent = True
        task.save()


    return redirect(request.META.get('HTTP_REFERER', '/'))
# ================= PROJECT =================

@login_required(login_url='/accounts/login/')
def project_list(request):

    user = request.user

    projects = Project.objects.filter(
        organization=user.organization
    )

    return render(request, 'projects/project01_list.html', {
        'projects': projects
    })


@login_required(login_url='/accounts/login/')
def create_project(request):
    user = request.user
    users = User.objects.filter(organization=user.organization)

    if request.method == "POST":
        project=Project.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            status=request.POST.get("status"),
            priority=request.POST.get("priority"),
            due_date=request.POST.get("due_date") or None,
            created_by=user,
            organization=user.organization
        )

        member_ids = request.POST.getlist('members')
        project.members.set(member_ids)


        return redirect('project_list')

    return render(request, 'projects/create_project.html', {
        'users': users   
    })

@login_required(login_url='/accounts/login/')
def update_project(request, project_id):
    user = request.user

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=user.organization
    )

    if request.method == "POST":
        project.name = request.POST.get("name")
        project.description = request.POST.get("description")
        project.status = request.POST.get("status")
        project.priority = request.POST.get("priority")
        project.due_date = request.POST.get("due_date") or None

        project.save()

        # 🔔 Notification: Project Updated
        for member in project.members.all():
            create_notification(
                 member,
                 f"Project updated: {project.name}"
            )

        return redirect('project_list')

    return render(request, 'projects/update_project.html', {
        'project': project
    })


@login_required(login_url='/accounts/login/')
def delete_project(request, project_id):
    

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=request.user.organization
    )

    project.delete()
    return redirect('project_list')


# ================= TASK CREATE =================

@login_required(login_url='/accounts/login/')
def create_task(request):

    user = request.user

    projects = Project.objects.filter(
        organization=user.organization
    ).order_by("name")

    tasks = Task.objects.filter(
        project__organization=user.organization
    )

    # Selected project from GET or POST
    selected_project_id = (
        request.POST.get("project")
        if request.method == "POST"
        else request.GET.get("project")
    )

    selected_project = None
    users = User.objects.none()

    # =========================================================
    # LOAD TEAM MEMBERS OF SELECTED PROJECT
    # =========================================================

    if selected_project_id:

        selected_project = get_object_or_404(
            Project,
            id=selected_project_id,
            organization=user.organization
        )

        users = User.objects.filter(
            project_memberships__team__project=selected_project,
            organization=user.organization,
            is_active=True
        ).distinct().select_related("role")

    # =========================================================
    # POST
    # =========================================================

    if request.method == "POST":

        title = request.POST.get("title")
        status = request.POST.get("status") or "todo"
        priority = request.POST.get("priority") or "medium"
        due_date = request.POST.get("due_date") or None

        reminder_raw = request.POST.get("reminder_date")
        reminder_date = None

        if reminder_raw:
            reminder_date = timezone.make_aware(
                datetime.fromisoformat(reminder_raw)
            )

        # -----------------------------------------------------
        # DUE DATE
        # -----------------------------------------------------

        if due_date:

            due_date_obj = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()

            if due_date_obj < date.today():

                messages.error(
                    request,
                    "Due date cannot be in past."
                )

                return redirect("create_task")

        # -----------------------------------------------------
        # REMINDER
        # -----------------------------------------------------

        if reminder_date:

            if reminder_date < timezone.now():

                messages.error(
                    request,
                    "Reminder cannot be in past."
                )

                return redirect("create_task")

        project_id = request.POST.get("project")
        assigned_to_id = request.POST.get("assigned_to")
        dependency_id = request.POST.get("dependency")

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if not title or not project_id:

            messages.error(
                request,
                "Title and Project required."
            )

            return redirect("create_task")

        # -----------------------------------------------------
        # PROJECT
        # -----------------------------------------------------

        project = get_object_or_404(
            Project,
            id=project_id,
            organization=user.organization
        )

        # -----------------------------------------------------
        # VERIFY ASSIGNED USER IS A TEAM MEMBER
        # -----------------------------------------------------

        assigned_to = None

        if assigned_to_id:

            assigned_to = User.objects.filter(
                id=assigned_to_id,
                organization=user.organization,
                is_active=True,
                project_memberships__team__project=project
            ).distinct().first()

            if not assigned_to:

                messages.error(
                    request,
                    "Selected user is not a member of this project's team."
                )

                return redirect(
                    f"/projects/tasks/create/?project={project.id}"
                )

        # -----------------------------------------------------
        # DEPENDENCY
        # -----------------------------------------------------

        dependency = None

        if dependency_id:

            dependency = Task.objects.filter(
                id=dependency_id,
                project=project
            ).first()

        # -----------------------------------------------------
        # CREATE TASK
        # -----------------------------------------------------

        task = Task.objects.create(
            title=title,
            project=project,
            organization=project.organization,
            assigned_to=assigned_to,
            status=status,
            priority=priority,
            due_date=due_date,
            reminder_date=reminder_date,
            dependency=dependency,
            order=0
        )

        # -----------------------------------------------------
        # ACTIVITY LOG
        # -----------------------------------------------------

        ActivityLog.objects.create(
            task=task,
            user=user,
            action="Task Created"
        )

        # -----------------------------------------------------
        # NOTIFICATION
        # -----------------------------------------------------

        if assigned_to:

            create_notification(
                assigned_to,
                f"You have been assigned a new task: {task.title}"
            )

        return redirect("tasks_list")

    # =========================================================
    # GET
    # =========================================================

    return render(
        request,
        "projects/create_task.html",
        {
            "projects": projects,
            "users": users,
            "tasks": tasks,
            "selected_project": selected_project,
        }
    )

# ================= KANBAN =================

@login_required(login_url='/accounts/login/')
def kanban_board(request):

    user = request.user

    projects = Project.objects.filter(organization=user.organization)

    search = request.GET.get('search')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    sort = request.GET.get('sort')

    project_data = []

    for project in projects:
        tasks = Task.objects.filter(project=project)

        if search:
            tasks = tasks.filter(
                Q(title__icontains=search) |
                Q(project__name__icontains=search) |
                Q(assigned_to__username__icontains=search)
            )

        if status:
            tasks = tasks.filter(status=status)

        if priority:
            tasks = tasks.filter(priority=priority)

        if sort == "priority":
            tasks = tasks.order_by(
                Case(
                    When(priority='high', then=0),
                    When(priority='medium', then=1),
                    When(priority='low', then=2),
                    output_field=IntegerField()
                )
            )

        project_data.append({
            'project': project,
            'todo': tasks.filter(status='todo').order_by('order'),
            'progress': tasks.filter(status='progress').order_by('order'),
            'done': tasks.filter(status='done').order_by('order'),
            'total_tasks': tasks.count(),
            'completed_tasks': tasks.filter(status='done').count(),
            'overdue_tasks': tasks.filter(
                due_date__lt=timezone.now().date()
            ).exclude(status='done')
        })

    return render(request, 'projects/member2/kanbanboard.html', {
        'project_data': project_data,
        'all_projects': projects
    })


# ================= UPDATE TASK STATUS =================

@login_required(login_url='/accounts/login/')
def update_task_status(request, task_id):
    user = request.user

    task = get_object_or_404(
        Task,
        id=task_id,
        project__organization=user.organization
    )

    old_status = task.status
    action = request.POST.get("action")

    if action == "forward":
        if task.status == "todo":
            task.status = "progress"
        elif task.status == "progress":
            task.status = "done"

    elif action == "backward":
        if task.status == "done":
            task.status = "progress"
        elif task.status == "progress":
            task.status = "todo"

    task.save()

    ActivityLog.objects.create(
        task=task,
        user=user,
        action=f"{old_status} → {task.status}"
    )

    # 🔔 Notification: Status Change
    if task.assigned_to:
        create_notification(
            task.assigned_to,
            f"Task moved from {old_status} to {task.status}: {task.title}"
      )

    return redirect('kanban')


# ================= EXPORT CSV =================

@login_required(login_url='/accounts/login/')
def export_tasks_csv(request):
    user = request.user

    tasks = Task.objects.filter(
        project__organization=user.organization
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Project', 'User', 'Status', 'Priority'])

    for t in tasks:
        writer.writerow([
            t.title,
            t.project.name,
            t.assigned_to.username if t.assigned_to else "",
            t.status,
            t.priority
        ])

    return response


# ================= PROJECT DETAIL =================

@login_required(login_url='/accounts/login/')
def project_detail(request, project_id):
    user = request.user

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=user.organization
    )

    tasks = Task.objects.filter(project=project)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks
    })


# ================= TASK LIST =================

@login_required(login_url='/accounts/login/')
def task_list(request):

    user = request.user

    tasks = Task.objects.filter(
        project__organization=user.organization
    )

    search = request.GET.get('search')
    if search:
       tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(project__name__icontains=search) |
            Q(assigned_to__username__icontains=search)
      )

    status = request.GET.get('status')
    priority = request.GET.get('priority')
    project_id = request.GET.get('project')
    member = request.GET.get('member')
    due = request.GET.get('due')

    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if project_id:
        tasks = tasks.filter(project__id=project_id)
    if member:
        tasks = tasks.filter(assigned_to__id=member)
    if due:
        tasks = tasks.filter(due_date=due)

    sort = request.GET.get('sort')

    if sort == 'new':
        tasks = tasks.order_by('-id')
    elif sort == 'old':
        tasks = tasks.order_by('id')
    elif sort == 'priority':
        tasks = tasks.order_by(
            Case(
                When(priority='high', then=0),
                When(priority='medium', then=1),
                When(priority='low', then=2),
                output_field=IntegerField()
            )
        )
    elif sort == 'project':
        tasks = tasks.order_by('project__name')
    elif sort == 'due':
        tasks = tasks.order_by('due_date')
    elif sort == 'status':
        tasks = tasks.order_by('status')

    projects = Project.objects.filter(organization=user.organization)
    users = User.objects.filter(organization=user.organization)


    return render(request, 'projects/project_task.html', {   
        'tasks': tasks,
        'projects': projects,
        'users': users,
        'overdue_tasks': tasks.filter(
            due_date__lt=timezone.now().date()
        ).exclude(status='done')
    })



# ================= TASK DETAIL =================

@login_required(login_url='/accounts/login/')
def task_detail(request, task_id):
    user = request.user

    task = get_object_or_404(
        Task,
        id=task_id,
        project__organization=user.organization
    )

    activities = ActivityLog.objects.filter(
        task=task
    ).order_by('-created_at')

    return render(request, 'projects/task_detail.html', {
        'task': task,
        'activities': activities
    })


# ================= UPDATE TASK =================

@login_required(login_url='/accounts/login/')
def update_task(request, task_id):
    user = request.user

    task = get_object_or_404(
        Task,
        id=task_id,
        project__organization=user.organization
    )

    if request.method == "POST":

        task.title = request.POST.get("title")
        task.description = request.POST.get("description")

        # =========================
        # SAFE PROJECT UPDATE
        # =========================

        project_id = request.POST.get("project")

        if project_id:
            task.project = get_object_or_404(
                Project,
                id=project_id,
                organization=user.organization
            )

        # =========================
        # ASSIGNED USER
        # =========================

        assigned_to_id = request.POST.get("assigned_to")

        if assigned_to_id:
            task.assigned_to = get_object_or_404(
                User,
                id=assigned_to_id,
                organization=user.organization
            )
        else:
            task.assigned_to = None

        # =========================
        # BASIC FIELDS
        # =========================

        task.status = request.POST.get(
            "status",
            task.status
        )

        task.priority = request.POST.get(
            "priority",
            task.priority
        )

        task.due_date = request.POST.get(
            "due_date"
        ) or None

        # =========================
        # REMINDER
        # =========================

        reminder_raw = request.POST.get("reminder_date")

        if reminder_raw:
            task.reminder_date = datetime.fromisoformat(
                reminder_raw
            )
        else:
            task.reminder_date = None

        # =========================
        # DEPENDENCY
        # =========================

        dependency_id = request.POST.get("dependency")

        if dependency_id:
            task.dependency = Task.objects.filter(
                id=dependency_id,
                project__organization=user.organization
            ).exclude(
                id=task.id
            ).first()
        else:
            task.dependency = None

        task.save()

        # =========================
        # ACTIVITY LOG
        # =========================

        ActivityLog.objects.create(
            task=task,
            user=user,
            action="Task Updated"
        )

        # =========================
        # NOTIFICATION
        # =========================

        if task.assigned_to:
            create_notification(
                task.assigned_to,
                f"Task updated: {task.title}"
            )

        return redirect(
            "task_detail",
            task.id
        )

    # =========================
    # GET REQUEST
    # =========================

    projects = Project.objects.filter(
        organization=user.organization
    )

    # All users belonging to the same organization
    users = User.objects.filter(
        organization=user.organization
    ).select_related("role")

    tasks = Task.objects.filter(
        project__organization=user.organization
    ).exclude(
        id=task.id
    )

    return render(
        request,
        "projects/update_task.html",
        {
            "task": task,
            "projects": projects,
            "users": users,
            "tasks": tasks,
        },
    )

# ================= DELETE TASK =================

@login_required(login_url='/accounts/login/')
def delete_task(request, task_id):
    user = request.user

    task = get_object_or_404(
        Task,
        id=task_id,
        project__organization=user.organization
    )

    if request.method == "POST":
        ActivityLog.objects.create(
            task=task,
            user=user,
            action="Task Deleted"
        )

        task.delete()
        return redirect('tasks_list')

    return render(request, 'projects/delete_task.html', {
        'task': task
    })

from django.http import JsonResponse
@login_required(login_url='/accounts/login/')
def get_project_team_members(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=request.user.organization
    )

    # Check whether this project has any team
    teams = Team.objects.filter(
        project=project
    )

    if not teams.exists():

        return JsonResponse({
            "has_team": False,
            "message": (
                "No team has been created for this project. "
                "Please create a team first."
            ),
            "members": []
        })

    # Get members belonging to teams of this project
    users = User.objects.filter(
        organization=request.user.organization,
        is_active=True,
        project_memberships__team__project=project
    ).distinct()

    members = []

    for user in users:

        membership = ProjectMember.objects.filter(
            team__project=project,
            user=user
        ).select_related("team").first()

        if user.first_name or user.last_name:
            name = f"{user.first_name} {user.last_name}".strip()
        else:
            name = user.username

        members.append({
            "id": user.id,
            "name": name,
            "email": user.email,
            "team": membership.team.name if membership else "",
            "team_role": membership.team_role if membership else "Member",
        })

    return JsonResponse({
        "has_team": True,
        "message": "",
        "members": members
    })


# ================= NOTIFICATIONS =================

@login_required(login_url='/accounts/login/')
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')


    return render(
        request,
        'projects/notifications.html',
        {
            'notifications': notifications
        }
    )

# ================= NOTIFICATIONS API =================


@login_required(login_url='/accounts/login/')
def get_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')


    data = []

    for notification in notifications:

        data.append({

            "id": notification.id,

            "message": notification.message,

            "is_read": notification.is_read,

            "created_at": notification.created_at.strftime(
                "%d %b %Y %H:%M"
            )

        })


    return JsonResponse({
    "notifications": data
})



@login_required(login_url='/accounts/login/')
def notification_count(request):

    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()


    return JsonResponse({

        "count": count

    })



@login_required(login_url='/accounts/login/')
def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )


    notification.is_read = True
    notification.save()


    return JsonResponse({

        "status": "success"

    })



@login_required(login_url='/accounts/login/')
def team_members(request):

    organization = request.user.organization

    projects = Project.objects.filter(
        organization=organization
    ).order_by("name")

    teams = Team.objects.filter(
        project__organization=organization
    ).select_related(
        "project",
        "created_by"
    ).prefetch_related(
        "members__user"
    ).order_by(
        "project__name",
        "name"
    )

    context = {
        "projects": projects,
        "teams": teams,
    }

    return render(
        request,
        "projects/team_members.html",
        context
    )

@login_required(login_url='/accounts/login/')
def create_team(request):

    organization = request.user.organization

    projects = Project.objects.filter(
        organization=organization
    ).order_by("name")

    organization_users = User.objects.filter(
        organization=organization,
        is_active=True
    ).select_related("role")

    if request.method == "POST":

        project_id = request.POST.get("project")
        team_name = request.POST.get("team_name", "").strip()

        member_ids = request.POST.getlist("members")

        if not project_id:
            messages.error(
                request,
                "Please select a project."
            )
            return redirect("create_team")

        if not team_name:
            messages.error(
                request,
                "Please enter a team name."
            )
            return redirect("create_team")

        if not member_ids:
            messages.error(
                request,
                "Please select at least one team member."
            )
            return redirect("create_team")

        project = get_object_or_404(
            Project,
            id=project_id,
            organization=organization
        )

        if Team.objects.filter(
            project=project,
            name__iexact=team_name
        ).exists():

            messages.error(
                request,
                "A team with this name already exists in this project."
            )

            return redirect("create_team")

        # =====================================================
        # CREATE TEAM
        # =====================================================

        team = Team.objects.create(
            project=project,
            name=team_name,
            created_by=request.user
        )


        # =====================================================
        # AUTOMATICALLY ADD ORGANIZATION ADMIN
        # =====================================================

        organization_admins = User.objects.filter(
            organization=organization,
            is_active=True,
            role__name__in=["Owner", "Admin"]
        )

        for user in organization_admins:
            ProjectMember.objects.get_or_create(
                team=team,
                user=user,
                defaults={
                    "team_role": "Member"
                }
            )


        # =====================================================
        # ADD SELECTED TEAM MEMBERS
        # =====================================================

        valid_users = User.objects.filter(
            id__in=member_ids,
            organization=organization,
            is_active=True
        ).select_related("role")


        for user in valid_users:

            # Don't create duplicate membership
            # if Admin was already selected manually.

            if ProjectMember.objects.filter(
                team=team,
                user=user
            ).exists():

                continue

            team_role = request.POST.get(
                f"team_role_{user.id}",
                "Member"
            )

            ProjectMember.objects.create(
                team=team,
                user=user,
                team_role=team_role
            )


        messages.success(
            request,
            f'Team "{team.name}" created successfully.'
        )

        return redirect("team_members")


    return render(
        request,
        "projects/create_team.html",
        {
            "projects": projects,
            "organization_users": organization_users,
        }
    )

@login_required(login_url="/accounts/login/")
def add_team_members(request, team_id):

    organization = request.user.organization

    team = get_object_or_404(
        Team,
        id=team_id,
        project__organization=organization
    )

    existing_member_ids = ProjectMember.objects.filter(
        team=team
    ).values_list(
        "user_id",
        flat=True
    )

    available_users = User.objects.filter(
        organization=organization,
        is_active=True
    ).exclude(
        id__in=existing_member_ids
    ).select_related("role")

    if request.method == "POST":

        member_ids = request.POST.getlist("members")

        if not member_ids:
            messages.error(
                request,
                "Please select at least one member."
            )
            return redirect(
                "add_team_members",
                team_id=team.id
            )

        valid_users = User.objects.filter(
            id__in=member_ids,
            organization=organization,
            is_active=True
        ).exclude(
            id__in=existing_member_ids
        )

        for user in valid_users:

            team_role = request.POST.get(
                f"team_role_{user.id}",
                "Member"
            )

            ProjectMember.objects.create(
                team=team,
                user=user,
                team_role=team_role
            )

        messages.success(
            request,
            "New team members added successfully."
        )

        return redirect(
            "team_members"
        )

    return render(
        request,
        "projects/add_team_members.html",
        {
            "team": team,
            "available_users": available_users,
        }
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Team


@login_required(login_url="/accounts/login/")
def team_detail(request, team_id):

    organization = request.user.organization

    team = get_object_or_404(
        Team.objects.select_related(
            "project",
            "created_by"
        ),
        id=team_id,
        project__organization=organization
    )

    members = team.members.select_related(
        "user",
        "user__role"
    ).all()

    return render(
        request,
        "projects/team_detail.html",
        {
            "team": team,
            "members": members,
        }
    )