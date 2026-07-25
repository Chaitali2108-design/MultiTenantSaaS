from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task


@login_required
def project_list(request):

    projects = Project.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/project_list.html', {
        'projects': projects
    })


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/task_list.html', {
        'tasks': tasks
    })


@login_required
def create_project(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        Project.objects.create(
            name=name,
            description=description,
            organization=request.user.organization,   # 🔥 AUTO
            created_by=request.user
        )

        return redirect('project_list')

    return render(request, 'projects/create_project.html')


@login_required
def create_task(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        project_id = request.POST.get('project')

        project = Project.objects.get(id=project_id)

        Task.objects.create(
            title=title,
            project=project,
            organization=request.user.organization,   # 🔥 AUTO
            assigned_to=request.user
        )

        return redirect('task_list')

    projects = Project.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/create_task.html', {
        'projects': projects
    })