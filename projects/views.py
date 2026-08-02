from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.http import HttpResponse
import csv

from .models import Project, Task, ActivityLog
from accounts.models import User
from django.contrib import messages


def get_user(request):
    user = User.objects.get(id=request.user.id)
    user.refresh_from_db()
    return user


# ================= PROJECT =================
def project_list(request):
    user = get_user(request)

    projects = Project.objects.filter(organization=user.organization)

    return render(request, 'projects/project01_list.html', {'projects': projects})


def create_project(request):
    user = get_user(request)

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


def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.name = request.POST.get("name")
        project.description = request.POST.get("description")
        project.status = request.POST.get("status")
        project.priority = request.POST.get("priority")
        project.due_date = request.POST.get("due_date") or None
        project.save()
        return redirect('project_list')

    return render(request, 'projects/update_project.html', {'project': project})


def delete_project(request, project_id):
    Project.objects.get(id=project_id).delete()
    return redirect('project_list')

# ================= TASK =================

def create_task(request):
    # 🔒 Multi-tenant safety (only current org data)
    print("Current User:", request.user)
    print("Organization:", request.user.organization)
    projects = Project.objects.filter(organization=request.user.organization)
    print(projects)
    users = User.objects.filter(organization=request.user.organization)
    tasks = Task.objects.filter(project__organization=request.user.organization)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        dependency_id = request.POST.get('dependency')

        # basic validation
        if not title or not project_id:
            messages.error(request, "Title and Project are required")
            return redirect('create_task')

        try:
            project = Project.objects.get(id=project_id, organization=request.user.organization)
        except Project.DoesNotExist:
            messages.error(request, "Invalid project")
            return redirect('create_task')

        assigned_to = None
        if assigned_to_id:
            assigned_to = User.objects.filter(
                id=assigned_to_id,
                organization=request.user.organization
            ).first()

        dependency = None
        if dependency_id:
            dependency = Task.objects.filter(
                id=dependency_id,
                project__organization=request.user.organization
            ).first()

        # create task
        task = Task.objects.create(
            title=title,
            project=project,
            organization=request.user.organization,
            assigned_to=assigned_to,
            status=status,
            priority=priority,
            due_date=due_date if due_date else None,
            dependency=dependency,
        )
        ActivityLog.objects.create(
            task=task,
            user=request.user,
            action="Task Created"
        )

        messages.success(request, "Task created successfully")
        return redirect('task_list')  # change if your URL name is different

    return render(request, 'projects/create_task.html', {
    'projects': projects,
    'users': users,
    'tasks': tasks
})

# ================= KANBAN =================

def kanban_board(request):

    user = get_user(request)

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
            'completed_tasks': tasks.filter(status='done').count()
        })

    return render(request, 'projects/member2/kanbanboard.html', {
        'project_data': project_data,
        'all_projects': projects
    })


# ================= UPDATE STATUS =================

def update_task_status(request, task_id):

    task = Task.objects.get(id=task_id)
    old = task.status

    action = request.POST.get("action")

    if action == "forward":
        task.status = "progress" if task.status == "todo" else "done"
    elif action == "backward":
        task.status = "progress" if task.status == "done" else "todo"

    task.save()

    ActivityLog.objects.create(
        task=task,
        user=request.user,
        action=f"{old} → {task.status}"
    )

    return redirect('kanban_board')


# ================= EXPORT =================

def export_tasks_csv(request):

    user = get_user(request)
    tasks = Task.objects.filter(organization=user.organization)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Project', 'User', 'Status', 'Priority'])

    for t in tasks:
        writer.writerow([t.title, t.project.name, t.assigned_to.username, t.status, t.priority])

    return response

#project_detail
def project_detail(request, project_id):

    user = get_user(request)

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=user.organization
    )

    if request.method == "POST":

        Task.objects.create(
            title=request.POST.get("title"),
            project=project,
            organization=user.organization,
            assigned_to=user,
            priority="medium"
        )

        return redirect('project_detail', project_id=project.id)


    tasks = Task.objects.filter(project=project)

    return render(
        request,
        'projects/project_detail.html',
        {
            'project': project,
            'tasks': tasks
        }
    )

    # ================= TASK LIST =================

def task_list(request):

    user = get_user(request)

    tasks = Task.objects.filter(
        project__organization=user.organization
    )

    # 🔍 SEARCH
    search = request.GET.get('search')
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # 🎯 FILTERS
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

    # 🔃 SORTING
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

    return render(
    request,
    'projects/project_task.html',
    {
        'tasks': tasks,
        'projects': projects,
        'users': users,
    }
)

# ================= TASK DETAIL =================

def task_detail(request, task_id):

    user = get_user(request)

    task = get_object_or_404(
        Task,
        id=task_id,
        organization=user.organization
    )

    activities = ActivityLog.objects.filter(
        task=task
    ).order_by('-created_at')


    return render(
        request,
        'projects/task_detail.html',
        {
            'task': task,
            'activities': activities
        }
    )


# ================= UPDATE TASK =================
def update_task(request, task_id):

    user = get_user(request)

    task = get_object_or_404(
        Task,
        id=task_id,
        organization=user.organization
    )

    if request.method == "POST":

        task.title = request.POST.get("title")
        task.description = request.POST.get("description")

        project_id = request.POST.get("project")
        task.project = Project.objects.get(
            id=project_id,
            organization=user.organization
        )

        assigned_to_id = request.POST.get("assigned_to")

        if assigned_to_id:
            task.assigned_to = User.objects.get(
                id=assigned_to_id,
                organization=user.organization
            )

        task.status = request.POST.get("status")
        task.priority = request.POST.get("priority")
        task.due_date = request.POST.get("due_date") or None

        dependency_id = request.POST.get("dependency")

        if dependency_id:
            task.dependency = Task.objects.get(id=dependency_id)
        else:
            task.dependency = None

        task.save()

        ActivityLog.objects.create(
            task=task,
            user=user,
            action="Task Updated"
        )

        return redirect("task_detail", task.id)

    projects = Project.objects.filter(
        organization=user.organization
    )

    users = User.objects.filter(
        organization=user.organization
    )

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

def delete_task(request, task_id):

    user = get_user(request)

    task = get_object_or_404(
        Task,
        id=task_id,
        organization=user.organization
    )


    if request.method == "POST":

        ActivityLog.objects.create(
            task=task,
            user=user,
            action="Task Deleted"
        )

        task.delete()

        return redirect(
            'task_list'
        )


    return render(
        request,
        'projects/delete_task.html',
        {
            'task': task
        }
    )