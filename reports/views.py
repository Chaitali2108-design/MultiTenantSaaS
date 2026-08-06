from django.shortcuts import render
from projects.models import Project, Task
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json
from django.db.models.functions import Lower



def reports(request):

    projects = Project.objects.all().order_by("-created_at")
    tasks = Task.objects.all().order_by("-created_at")

    # -------------------
    # Monthly Task Data
    # -------------------

    monthly_tasks = (
        Task.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    month_names = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    task_dict = {i:0 for i in range(1,13)}

    for item in monthly_tasks:
        if item["month"]:
            task_dict[item["month"].month] = item["count"]

    months = month_names
    task_counts = [task_dict[i] for i in range(1,13)]
    
    monthly_projects = (
    Project.objects
    .annotate(month=TruncMonth("created_at"))
    .values("month")
    .annotate(count=Count("id"))
    .order_by("month")
    )

    project_dict = {i:0 for i in range(1,13)}

    for item in monthly_projects:
        if item["month"]:
            project_dict[item["month"].month] = item["count"]

    project_months = month_names
    project_counts = [project_dict[i] for i in range(1,13)]

    priority_data = (
        Task.objects
        .annotate(priority_name=Lower("priority"))
        .values("priority_name")
        .annotate(count=Count("id"))
    )

    priority_labels = []
    priority_counts = []

    for item in priority_data:
        priority_labels.append(item["priority_name"].title())
        priority_counts.append(item["count"])

    user_data = (
    Task.objects
    .values("assigned_to__username")
    .annotate(count=Count("id"))
    )

    user_labels = []
    user_counts = []

    for item in user_data:

        if item["assigned_to__username"]:
            user_labels.append(item["assigned_to__username"])
        else:
            user_labels.append("Unassigned")

        user_counts.append(item["count"])


    project_task_data = (
    Task.objects
    .values("project__name")
    .annotate(count=Count("id"))
    )

    project_labels = []
    project_task_counts = []

    for item in project_task_data:
        project_labels.append(item["project__name"])
        project_task_counts.append(item["count"])

    due_tasks = Task.objects.exclude(due_date=None).count()

    completed_tasks = Task.objects.filter(status="done").count()

    # -------------------
    # Filters
    # -------------------

    selected_month = request.GET.get("month")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if selected_month:
        tasks = tasks.filter(created_at__month=selected_month)
        projects = projects.filter(created_at__month=selected_month)

    if from_date:
        tasks = tasks.filter(created_at__date__gte=from_date)
        projects = projects.filter(created_at__date__gte=from_date)

    if to_date:
        tasks = tasks.filter(created_at__date__lte=to_date)
        projects = projects.filter(created_at__date__lte=to_date)

    # -------------------
    # Dashboard Cards
    # -------------------

    total_projects = projects.count()
    total_tasks = tasks.count()

    completed_tasks = tasks.filter(status="done").count()
    pending_tasks = total_tasks - completed_tasks

    status_map = {
        "todo": 0,
        "progress": 0,
        "done": 0,
    }

    for task in Task.objects.all():
        status = task.status.lower()
        if status in status_map:
            status_map[status] += 1

    status_labels = ["Todo", "Progress", "Done"]
    status_counts = [
        status_map["todo"],
        status_map["progress"],
        status_map["done"],
    ]

    context = {

    "total_projects": total_projects,
    "total_tasks": total_tasks,
    "completed_tasks": completed_tasks,
    "pending_tasks": pending_tasks,

    "months": json.dumps(months),
    "task_counts": json.dumps(task_counts),

    "project_months": json.dumps(project_months),
    "project_counts": json.dumps(project_counts),

    "priority_labels": json.dumps(priority_labels),
    "priority_counts": json.dumps(priority_counts),

    "user_labels": json.dumps(user_labels),
    "user_counts": json.dumps(user_counts),

    "project_labels": json.dumps(project_labels),
    "project_task_counts": json.dumps(project_task_counts),

    "due_tasks": due_tasks,

    "status_labels": json.dumps(status_labels),
    "status_counts": json.dumps(status_counts),

    "selected_month": selected_month,
    "from_date": from_date,
    "to_date": to_date,
}

    return render(request, "reports/reports.html", context)