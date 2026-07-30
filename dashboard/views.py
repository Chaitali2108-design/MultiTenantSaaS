from django.shortcuts import render
def dashboard(request):
    return render(request, 'dashboard.html')
def project_list(request):
    return render(request, 'projects/project_list.html')

def task_list(request):
    return render(request, 'tasks/task_list.html')

def kanban(request):
    return render(request, 'tasks/kanban.html')

def tasks(request):
    return render(request, "tasks/tasks.html")

def reports(request):
    return render(request, "reports/reports.html")

def team_members(request):
    return render(request, 'team_members/team_members.html')

def profile(request):
    return render(request, 'profile/profile.html')

def settings(request):
    return render(request, 'settings/settings.html')

def organization(request):
    return render(request, "organizations/organization.html")

def login(request):
    return render(request, "registration/login.html")