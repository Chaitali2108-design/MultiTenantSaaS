from django.shortcuts import render
from projects.models import Project, Task


def reports(request):

    projects = Project.objects.all().order_by("-created_at")

    
    context = {

        "projects": projects,

    }

    return render(
        request,
        "reports/reports.html",
        context
    )
