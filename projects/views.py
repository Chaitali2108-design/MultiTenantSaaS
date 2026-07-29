from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.utils.timezone import now
from datetime import timedelta

from .models import Project, Task
from accounts.models import User


# =========================
# PROJECT LIST
# =========================
def project_list(request):

    projects = Project.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/project01_list.html', {
        'projects': projects
    })


# =========================
# CREATE PROJECT
# =========================
def create_project(request):

    if request.method == "POST":

        Project.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            organization=request.user.organization,
            created_by=request.user
        )

        return redirect('/projects/')

    return render(request, 'projects/create_project.html')


# =========================
# TASK LIST
# =========================
def task_list(request):

    tasks = Task.objects.filter(
        organization=request.user.organization
    )

    return render(request, 'projects/task_list.html', {
        'tasks': tasks
    })


# =========================
# CREATE TASK
# =========================
def create_task(request):

    if request.user.organization is None:

        return render(
            request,
            'projects/create_task.html',
            {
                'error': 'Assign organization first'
            }
        )


    projects = Project.objects.filter(
        organization=request.user.organization
    )


    if request.method == "POST":

        project = get_object_or_404(
            Project,
            id=request.POST.get('project'),
            organization=request.user.organization
        )


        Task.objects.create(

            title=request.POST.get('title'),

            project=project,

            organization=request.user.organization,

            assigned_to=request.user,

            priority=request.POST.get('priority'),

            due_date=request.POST.get('due_date') or None
        )


        return redirect('/projects/tasks/')


    return render(
        request,
        'projects/create_task.html',
        {
            'projects': projects
        }
    )



# =========================
# PROJECT DETAIL
# =========================
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        organization=request.user.organization
    )


    tasks = Task.objects.filter(
        project=project,
        organization=request.user.organization
    )


    return render(
        request,
        'projects/project_detail.html',
        {
            'project': project,
            'tasks': tasks
        }
    )



# =========================
# TASK DETAIL
# =========================
def task_detail(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        organization=request.user.organization
    )


    return render(
        request,
        'projects/task_detail.html',
        {
            'task': task
        }
    )



# =========================
# UPDATE TASK STATUS
# =========================
def update_task_status(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        organization=request.user.organization
    )


    if request.method == "POST":

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


    return redirect('/projects/kanban/')

# =========================
# KANBAN BOARD
# SEARCH + FILTER + SORT
# =========================
def kanban_board(request):

    projects = Project.objects.filter(
        organization=request.user.organization
    )


    selected_project = request.GET.get('project')


    if selected_project:

        projects = projects.filter(
            id=selected_project
        )


    search = request.GET.get('search')

    status = request.GET.get('status')

    priority = request.GET.get('priority')

    member = request.GET.get('member')

    due_filter = request.GET.get('due')

    sort = request.GET.get('sort')


    project_data = []



    for project in projects:


        tasks = Task.objects.filter(

            project=project,

            organization=request.user.organization

        )



        # =========================
        # SEARCH
        # =========================

        if search:


            words = search.split()


            for word in words:


                tasks = tasks.filter(

                    Q(title__icontains=word) |

                    Q(project__name__icontains=word) |

                    Q(assigned_to__username__icontains=word)

                )



        # =========================
        # FILTER STATUS
        # =========================

        if status:

            tasks = tasks.filter(
                status=status
            )



        # =========================
        # FILTER PRIORITY
        # =========================

        if priority:

            tasks = tasks.filter(
                priority=priority
            )



        # =========================
        # FILTER MEMBER
        # =========================

        if member:

            tasks = tasks.filter(
                assigned_to_id=member
            )



        # =========================
        # FILTER DUE DATE
        # =========================

        if due_filter == "today":

            tasks = tasks.filter(
                due_date=now().date()
            )


        elif due_filter == "overdue":

            tasks = tasks.filter(

                due_date__lt=now().date(),

                status__in=[
                    "todo",
                    "progress"
                ]

            )


        elif due_filter == "week":

            tasks = tasks.filter(

                due_date__lte=
                now().date() + timedelta(days=7)

            )



        # =========================
        # SORTING
        # =========================

        if sort == "newest":

            tasks = tasks.order_by(
                '-created_at'
            )


        elif sort == "oldest":

            tasks = tasks.order_by(
                'created_at'
            )


        elif sort == "due_date":

            tasks = tasks.order_by(
                'due_date'
            )


        elif sort == "priority":

            tasks = tasks.order_by(

                Case(

                    When(
                        priority='high',
                        then=0
                    ),

                    When(
                        priority='medium',
                        then=1
                    ),

                    When(
                        priority='low',
                        then=2
                    ),

                    output_field=IntegerField()

                )

            )


        elif sort == "project_name":

            tasks = tasks.order_by(
                'project__name'
            )


        elif sort == "status":

            tasks = tasks.order_by(

                Case(

                    When(
                        status='done',
                        then=0
                    ),

                    When(
                        status='progress',
                        then=1
                    ),

                    When(
                        status='todo',
                        then=2
                    ),

                    output_field=IntegerField()

                )

            )


        elif sort == "completion":

            tasks = tasks.order_by(
                'status'
            )



        if tasks.exists():


            project_data.append({

                'project': project,


                'todo': tasks.filter(
                    status='todo'
                ),


                'progress': tasks.filter(
                    status='progress'
                ),


                'done': tasks.filter(
                    status='done'
                ),


                'total_tasks':
                    tasks.count(),


                'completed_tasks':
                    tasks.filter(
                        status='done'
                    ).count()

            })



    return render(

        request,

        'projects/member2/kanbanboard.html',

        {


            'project_data':
                project_data,


            'all_projects':

                Project.objects.filter(

                    organization=request.user.organization

                ),


            'users':

                User.objects.filter(

                    organization=request.user.organization

                ),


            'selected_project':
                selected_project,


            'sort':
                sort

        }

    )



# =========================
# DASHBOARD
# =========================
def dashboard(request):

    tasks = Task.objects.filter(
        organization=request.user.organization
    )


    return render(

        request,

        'projects/dashboard.html',

        {


            'todo':
                tasks.filter(
                    status='todo'
                ).count(),


            'progress':
                tasks.filter(
                    status='progress'
                ).count(),


            'done':
                tasks.filter(
                    status='done'
                ).count()


        }

    )