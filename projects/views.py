from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import csv
from datetime import datetime, date

from .models import Project, Task, ActivityLog
from accounts.models import User


# ================= REMINDER CHECK =================
def check_reminders(request):
    now = timezone.now()

    tasks = Task.objects.filter(
        reminder_date__lte=now,
        reminder_sent=False
    )

    for task in tasks:

        print("REMINDER FOUND:", task.title)

        if task.priority == "high":
            message = f"🚨 HIGH PRIORITY Reminder: {task.title}"

        elif task.priority == "medium":
            message = f"⚠️ Reminder: {task.title}"

        else:
            message = f"🔔 Reminder: {task.title}"

        messages.warning(
            request,
            message
        )

        task.reminder_sent = True
        task.save()
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

    if request.method == "POST":
        Project.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            status=request.POST.get("status"),
            priority=request.POST.get("priority"),
            due_date=request.POST.get("due_date") or None,
            created_by=user,
            organization=user.organization
        )

        return redirect('project_list')

    return render(request, 'projects/create_project.html')


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
        return redirect('project_list')

    return render(request, 'projects/update_project.html', {
        'project': project
    })


@login_required(login_url='/accounts/login/')
def delete_project(request, project_id):
    user = request.user

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=user.organization
    )

    project.delete()
    return redirect('project_list')


# ================= TASK CREATE =================

@login_required(login_url='/accounts/login/')
def create_task(request):

    user = request.user

    # 🔒 Multi-tenant safety (only current org data)

    print("Current User:", request.user.username)
    print("Organization:", request.user.organization)

    projects = Project.objects.filter(
        organization=request.user.organization
    )

    print(projects)

    users = User.objects.filter(
        organization=request.user.organization
    )

    tasks = Task.objects.filter(
        project__organization=request.user.organization
    )

    print("Projects Count:", projects.count())
    print("Users Count:", users.count())
    print("Tasks Count:", tasks.count())
  

    if request.method == "POST":

        title = request.POST.get('title')
        status = request.POST.get('status') or 'todo'
        priority = request.POST.get('priority') or 'medium'
        due_date = request.POST.get('due_date') or None

        reminder_raw = request.POST.get('reminder_date')
        reminder_date = None

        if reminder_raw:
            reminder_date = timezone.make_aware(
                datetime.fromisoformat(reminder_raw)
            )
        # ✅ FIXED VALIDATION (INSIDE POST)
        if due_date:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()

            if due_date_obj < date.today():
                messages.error(request, "Due date cannot be in past")
                return redirect('create_task')

        if reminder_date:
            if reminder_date < timezone.now():
                messages.error(request, "Reminder cannot be in past")
                return redirect('create_task')

        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        dependency_id = request.POST.get('dependency')

        if not title or not project_id:
            messages.error(request, "Title and Project required")
            return redirect('create_task')

        project = get_object_or_404(
            Project,
            id=project_id,
            organization=user.organization
        )

        assigned_to = None
        if assigned_to_id:
            assigned_to = User.objects.filter(
                id=assigned_to_id,
                organization=user.organization
            ).first()

        dependency = None
        if dependency_id:
            dependency = Task.objects.filter(
                id=dependency_id,
                project__organization=user.organization
            ).first()

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

        ActivityLog.objects.create(
            task=task,
            user=user,
            action="Task Created"
        )

        return redirect('tasks_list')

    return render(request, 'projects/create_task.html', {

        'projects': projects,
        'users': users,
        'tasks': tasks
    })


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

        # ✅ SAFE PROJECT UPDATE
        project_id = request.POST.get("project")
        if project_id:
            task.project = get_object_or_404(
                Project,
                id=project_id,
                organization=user.organization
            )

        # ✅ ASSIGNED USER
        assigned_to_id = request.POST.get("assigned_to")
        if assigned_to_id:
            task.assigned_to = get_object_or_404(
                User,
                id=assigned_to_id,
                organization=user.organization
            )
        else:
            task.assigned_to = None

        # ✅ BASIC FIELDS
        task.status = request.POST.get("status", task.status)
        task.priority = request.POST.get("priority", task.priority)
        task.due_date = request.POST.get("due_date") or None

        # ✅ REMINDER
        reminder_raw = request.POST.get("reminder_date")
        if reminder_raw:
            task.reminder_date = datetime.fromisoformat(reminder_raw)

        # ✅ DEPENDENCY
        dependency_id = request.POST.get("dependency")
        if dependency_id:
            task.dependency = Task.objects.filter(
                id=dependency_id,
                project__organization=user.organization
            ).first()
        else:
            task.dependency = None

        task.save()

        ActivityLog.objects.create(
            task=task,
            user=user,
            action="Task Updated"
        )

        return redirect("task_detail", task.id)

    # GET REQUEST
    projects = Project.objects.filter(organization=user.organization)
    users = User.objects.filter(organization=user.organization)
    tasks = Task.objects.filter(
        project__organization=user.organization
    ).exclude(id=task.id)

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