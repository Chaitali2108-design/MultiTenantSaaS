from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task


# PROJECT LIST
def project_list(request):
    projects = Project.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/project01_list.html', {
        'projects': projects
    })


# CREATE PROJECT
def create_project(request):
    if request.method == 'POST':

        Project.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            organization=request.user.organization,
            created_by=request.user
        )

        return redirect('/projects/')

    return render(request, 'projects/create_project.html')


# TASK LIST
def task_list(request):
    tasks = Task.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/task_list.html', {
        'tasks': tasks
    })


# KANBAN BOARD
def kanban_board(request):

    tasks = Task.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/member2/kanbanboard.html', {

        'todo': tasks.filter(status='todo'),

        'progress': tasks.filter(status='progress'),

        'done': tasks.filter(status='done'),
    })


# TASK DETAIL PAGE
# CARD CLICK ONLY OPENS THIS PAGE
def task_detail(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        organization=request.user.organization
    )

    return render(request, 'projects/task_detail.html', {
        'task': task
    })


# MOVE TASK STATUS
# ONLY BUTTON CLICK SHOULD CALL THIS
def update_task_status(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        organization=request.user.organization
    )

    if request.method == "POST":

        if task.status == "todo":
            task.status = "progress"

        elif task.status == "progress":
            task.status = "done"

        task.save()

    return redirect('/projects/kanban/')


# CREATE TASK
def create_task(request):

    if request.user.organization is None:

        return render(request, 'projects/create_task.html', {
            'error': 'Assign organization first'
        })


    projects = Project.objects.filter(
        organization=request.user.organization
    )


    if request.method == 'POST':

        project = get_object_or_404(
            Project,
            id=request.POST.get('project'),
            organization=request.user.organization
        )


        Task.objects.create(
            title=request.POST.get('title'),
            project=project,
            organization=request.user.organization,
            assigned_to=request.user
        )


        return redirect('/projects/tasks/')


    return render(request, 'projects/create_task.html', {
        'projects': projects
    })


# PROJECT DETAIL
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=request.user.organization
    )


    if request.method == "POST":

        Task.objects.create(
            title=request.POST.get('title'),
            project=project,
            organization=request.user.organization,
            assigned_to=request.user
        )


        return redirect(f'/projects/{project.id}/')


    tasks = Task.objects.filter(
        project=project,
        organization=request.user.organization
    )


    return render(request, 'projects/project_detail.html', {

        'project': project,

        'tasks': tasks
    })