from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Project, Task


# ================= PROJECT LIST =================
@login_required
def project_list(request):
    projects = Project.objects.filter(
        organization=request.user.organization
    )
    return render(request, 'projects/project_list.html', {
        'projects': projects
    })


# ================= TASK LIST =================
@login_required
def task_list(request):
    tasks = Task.objects.filter(
        organization=request.user.organization,
        assigned_to=request.user
    )
    return render(request, 'projects/task_list.html', {
        'tasks': tasks
    })


# ================= CREATE PROJECT =================
from accounts.models import User

@login_required
def create_project(request):

    user = User.objects.get(id=request.user.id)  # fresh from DB

    if user.organization is None:
        return render(request, 'projects/create_project.html', {
            'error': 'Organization not assigned'
        })

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        Project.objects.create(
            name=name,
            description=description,
            organization=user.organization,
            created_by=user
        )

        return redirect('project_list')

    return render(request, 'projects/create_project.html')


# ================= CREATE TASK =================
@login_required
def create_task(request):

    if request.user.organization is None:
        return render(request, 'projects/create_task.html', {
            'error': '⚠️ Please assign organization in admin first'
        })

    if request.method == 'POST':
        title = request.POST.get('title')
        project_id = request.POST.get('project')

        project = Project.objects.get(
            id=project_id,
            organization=request.user.organization
        )

        Task.objects.create(
            title=title,
            project=project,
            organization=request.user.organization,
            assigned_to=request.user
        )

        return redirect('task_list')

    projects = Project.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/create_task.html', {
        'projects': projects
    })
