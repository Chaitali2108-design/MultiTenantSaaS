from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth, Lower

from projects.models import Project, Task
import csv
from django.http import HttpResponse
from openpyxl import Workbook

import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)


def reports(request):

    # ==================================================
    # FILTER VALUES
    # ==================================================

    selected_project = request.GET.get("project")
    selected_month = request.GET.get("month")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    # ==================================================
    # ALL PROJECTS FOR DROPDOWN
    # ==================================================

    all_projects = Project.objects.all().order_by("name")

    # ==================================================
    # BASE QUERYSETS
    # ==================================================

    projects = Project.objects.all()
    tasks = Task.objects.all()

    # ==================================================
    # PROJECT FILTER
    # ==================================================

    if selected_project:
        projects = projects.filter(id=selected_project)
        tasks = tasks.filter(project_id=selected_project)

    # ==================================================
    # MONTH FILTER
    # ==================================================

    if selected_month:
        projects = projects.filter(
            created_at__month=selected_month
        )

        tasks = tasks.filter(
            created_at__month=selected_month
        )

    # ==================================================
    # FROM DATE FILTER
    # ==================================================

    if from_date:
        projects = projects.filter(
            created_at__date__gte=from_date
        )

        tasks = tasks.filter(
            created_at__date__gte=from_date
        )

    # ==================================================
    # TO DATE FILTER
    # ==================================================

    if to_date:
        projects = projects.filter(
            created_at__date__lte=to_date
        )

        tasks = tasks.filter(
            created_at__date__lte=to_date
        )

    

    # ==================================================
# SUMMARY CARDS
# ==================================================

    total_projects = projects.count()

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        status__iexact="done"
    ).count()

    pending_tasks = total_tasks - completed_tasks

    # ==================================================
# CARD PERCENTAGES
# ==================================================

    if total_tasks > 0:
        completion_percentage = round(
            (completed_tasks / total_tasks) * 100,
            1
        )

        pending_percentage = round(
            (pending_tasks / total_tasks) * 100,
            1
        )
    else:
        completion_percentage = 0
        pending_percentage = 0


# ==================================================
# CURRENT MONTH / PREVIOUS MONTH
# ==================================================

    from django.utils import timezone

    today = timezone.now()

    current_month = today.month
    current_year = today.year

    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year


# ==================================================
# PROJECT MONTHLY CHANGE
# ==================================================

    current_month_projects = Project.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    ).count()

    previous_month_projects = Project.objects.filter(
        created_at__year=previous_year,
        created_at__month=previous_month
    ).count()

    if previous_month_projects == 0:
        project_change = 100 if current_month_projects > 0 else 0
    else:
        project_change = (
            (current_month_projects - previous_month_projects)
            / previous_month_projects
        ) * 100

    project_change = round(project_change, 1)


# ==================================================
# TASK MONTHLY CHANGE
# ==================================================

    current_month_tasks = Task.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    ).count()

    previous_month_tasks = Task.objects.filter(
        created_at__year=previous_year,
        created_at__month=previous_month
    ).count()

    if previous_month_tasks == 0:
        task_change = 100 if current_month_tasks > 0 else 0
    else:
        task_change = (
            (current_month_tasks - previous_month_tasks)
            / previous_month_tasks
        ) * 100

    task_change = round(task_change, 1)


# ==================================================
# COMPLETION PERCENTAGE
# ==================================================

    if total_tasks > 0:
        completion_percentage = round(
            (completed_tasks / total_tasks) * 100,
            1
        )
    else:
        completion_percentage = 0


# ==================================================
# PENDING PERCENTAGE
# ==================================================

    if total_tasks > 0:
        pending_percentage = round(
            (pending_tasks / total_tasks) * 100,
            1
        )
    else:
        pending_percentage = 0

    # ==================================================
    # MONTH NAMES
    # ==================================================

    month_names = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    # ==================================================
    # MONTHLY TASKS
    # ==================================================

    monthly_tasks = (
        tasks
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    task_dict = {
        i: 0 for i in range(1, 13)
    }

    for item in monthly_tasks:

        if item["month"]:
            task_dict[
                item["month"].month
            ] = item["count"]

    months = month_names

    task_counts = [
        task_dict[i]
        for i in range(1, 13)
    ]

    # ==================================================
# MONTHLY COMPLETED TASKS
# ==================================================

    monthly_completed_tasks = (
        tasks
        .filter(status__iexact="done")
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    completed_task_dict = {
        i: 0 for i in range(1, 13)
    }

    for item in monthly_completed_tasks:

        if item["month"]:
            completed_task_dict[
                item["month"].month
            ] = item["count"]

    completed_task_counts = [
        completed_task_dict[i]
        for i in range(1, 13)
    ]

    # ==================================================
    # MONTHLY PROJECTS
    # ==================================================

    monthly_projects = (
        projects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    project_dict = {
        i: 0 for i in range(1, 13)
    }

    for item in monthly_projects:

        if item["month"]:
            project_dict[
                item["month"].month
            ] = item["count"]

    project_months = month_names

    project_counts = [
        project_dict[i]
        for i in range(1, 13)
    ]

    # ==================================================
    # PRIORITY DISTRIBUTION
    # ==================================================

    priority_data = (
        tasks
        .annotate(
            priority_name=Lower("priority")
        )
        .values("priority_name")
        .annotate(count=Count("id"))
        .order_by("priority_name")
    )

    priority_labels = []
    priority_counts = []

    for item in priority_data:

        priority = item["priority_name"]

        if priority:
            priority_labels.append(
                priority.title()
            )
        else:
            priority_labels.append(
                "No Priority"
            )

        priority_counts.append(
            item["count"]
        )

    # ==================================================
    # TASKS PER USER
    # ==================================================

    user_data = (
        tasks
        .values("assigned_to__username")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    user_labels = []
    user_counts = []

    for item in user_data:

        username = item[
            "assigned_to__username"
        ]

        if username:
            user_labels.append(username)
        else:
            user_labels.append("Unassigned")

        user_counts.append(
            item["count"]
        )

    # ==================================================
    # TASKS PER PROJECT
    # ==================================================

    project_task_data = (
        tasks
        .values("project__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    project_labels = []
    project_task_counts = []

    for item in project_task_data:

        project_name = item["project__name"]

        if project_name:
            project_labels.append(
                project_name
            )
        else:
            project_labels.append(
                "No Project"
            )

        project_task_counts.append(
            item["count"]
        )

    # ==================================================
    # DUE TASKS
    # ==================================================

    from django.utils import timezone
    # ==================================================
# DUE / PENDING TASKS
# ==================================================

    today = timezone.now().date()

    due_tasks = tasks.filter(
        due_date__isnull=False,
        due_date__lte=today
    ).exclude(
        status__iexact="done"
    ).count()

    # ==================================================
    # TASK STATUS
    # ==================================================

    todo_tasks = tasks.filter(
        status__iexact="todo"
    ).count()

    progress_tasks = tasks.filter(
        status__iexact="progress"
    ).count()

    done_tasks = tasks.filter(
        status__iexact="done"
    ).count()

    status_labels = [
        "Todo",
        "In Progress",
        "Completed"
    ]

    status_counts = [
        todo_tasks,
        progress_tasks,
        done_tasks
    ]

    # ==================================================
    # CONTEXT
    # ==================================================

    context = {

            # Summary cards
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,

            "project_change": project_change,
            "task_change": task_change,
            "completion_percentage": completion_percentage,
            "pending_percentage": pending_percentage,

            # Project filter
            "all_projects": all_projects,
            "selected_project": selected_project,

            # Month filter
            "selected_month": selected_month,

            # Date filters
            "from_date": from_date,
            "to_date": to_date,

            # Monthly tasks
            "months": json.dumps(months),
            "task_counts": json.dumps(task_counts),
            "completed_task_counts": json.dumps(completed_task_counts),

            # Monthly projects
            "project_months": json.dumps(
                project_months
            ),
            "project_counts": json.dumps(
                project_counts
            ),

            # Priority
            "priority_labels": json.dumps(
                priority_labels
            ),
            "priority_counts": json.dumps(
                priority_counts
            ),

            # Users
            "user_labels": json.dumps(
                user_labels
            ),
            "user_counts": json.dumps(
                user_counts
            ),

            # Projects
            "project_labels": json.dumps(
                project_labels
            ),
            "project_task_counts": json.dumps(
                project_task_counts
            ),

            # Due
            "due_tasks": due_tasks,

            # Status
            "status_labels": json.dumps(
                status_labels
            ),
            "status_counts": json.dumps(
                status_counts
            ),
    }

    return render(
            request,
            "reports/reports.html",
            context
    )

def export_report(request):

    selected_project = request.GET.get("project")
    selected_month = request.GET.get("month")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    export_format = request.GET.get("format")

    # -----------------------------
    # Base querysets
    # -----------------------------

    projects = Project.objects.all()
    tasks = Task.objects.all()

    # -----------------------------
    # Project filter
    # -----------------------------

    if selected_project:
        projects = projects.filter(id=selected_project)
        tasks = tasks.filter(project_id=selected_project)

    # -----------------------------
    # Month filter
    # -----------------------------

    if selected_month:
        projects = projects.filter(
            created_at__month=selected_month
        )

        tasks = tasks.filter(
            created_at__month=selected_month
        )

    # -----------------------------
    # From date
    # -----------------------------

    if from_date:
        projects = projects.filter(
            created_at__date__gte=from_date
        )

        tasks = tasks.filter(
            created_at__date__gte=from_date
        )

    # -----------------------------
    # To date
    # -----------------------------

    if to_date:
        projects = projects.filter(
            created_at__date__lte=to_date
        )

        tasks = tasks.filter(
            created_at__date__lte=to_date
        )

    # ==================================================
    # CSV EXPORT
    # ==================================================

    if export_format == "csv":

        response = HttpResponse(
            content_type="text/csv"
        )

        response["Content-Disposition"] = (
            'attachment; filename="report.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            "Project",
            "Task",
            "Assigned To",
            "Priority",
            "Status",
            "Due Date",
            "Created At",
        ])

        for task in tasks.select_related(
            "project",
            "assigned_to"
        ):

            writer.writerow([
                task.project.name if task.project else "No Project",
                task.title,
                task.assigned_to.username
                if task.assigned_to
                else "Unassigned",
                task.priority or "No Priority",
                task.status,
                task.due_date or "",
                task.created_at,
            ])

        return response

    # ==================================================
    # EXCEL EXPORT
    # ==================================================

    if export_format == "excel":

        workbook = Workbook()

        worksheet = workbook.active
        worksheet.title = "Report"

        worksheet.append([
            "Project",
            "Task",
            "Assigned To",
            "Priority",
            "Status",
            "Due Date",
            "Created At",
        ])

        for task in tasks.select_related(
            "project",
            "assigned_to"
        ):

            worksheet.append([
                task.project.name if task.project else "No Project",
                task.title,
                task.assigned_to.username
                if task.assigned_to
                else "Unassigned",
                task.priority or "No Priority",
                task.status,
                str(task.due_date or ""),
                str(task.created_at),
            ])

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

        response["Content-Disposition"] = (
            'attachment; filename="report.xlsx"'
        )

        workbook.save(response)

        return response
        # ==================================================
    # PDF EXPORT
    # ==================================================

    if export_format == "pdf":

        response = HttpResponse(
            content_type="application/pdf"
        )

        response["Content-Disposition"] = (
            'attachment; filename="report.pdf"'
        )

        document = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25,
        )

        styles = getSampleStyleSheet()

        elements = []

        # PDF title
        title = Paragraph(
            "Reports & Analytics",
            styles["Title"]
        )

        elements.append(title)

        elements.append(
            Spacer(1, 15)
        )

        # Report information
        filter_text = []

        if selected_project:
            project = Project.objects.filter(
                id=selected_project
            ).first()

            if project:
                filter_text.append(
                    f"Project: {project.name}"
                )

        if selected_month:
            filter_text.append(
                f"Month: {selected_month}"
            )

        if from_date:
            filter_text.append(
                f"From: {from_date}"
            )

        if to_date:
            filter_text.append(
                f"To: {to_date}"
            )

        if filter_text:

            elements.append(
                Paragraph(
                    " | ".join(filter_text),
                    styles["Normal"]
                )
            )

            elements.append(
                Spacer(1, 15)
            )

        # Table header
        data = [[
            "Project",
            "Task",
            "Assigned To",
            "Priority",
            "Status",
            "Due Date",
            "Created At",
        ]]

        # Table rows
        for task in tasks.select_related(
            "project",
            "assigned_to"
        ):

            data.append([
                task.project.name
                if task.project
                else "No Project",

                task.title,

                task.assigned_to.username
                if task.assigned_to
                else "Unassigned",

                task.priority
                if task.priority
                else "No Priority",

                task.status,

                str(task.due_date)
                if task.due_date
                else "",

                str(task.created_at),
            ])

        # Create table
        table = Table(
            data,
            repeatRows=1,
            colWidths=[
                90,
                150,
                90,
                70,
                70,
                80,
                120,
            ]
        )

        # Table styling
        table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0f766e")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#f8fafc")
                    ]
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
            ])
        )

        elements.append(table)

        document.build(elements)

        return response

    # ==================================================
    # INVALID FORMAT
    # ==================================================

    return HttpResponse(
        "Invalid export format.",
        status=400
    )