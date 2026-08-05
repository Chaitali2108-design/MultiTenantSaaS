from django.urls import path
from . import views
from projects import views as project_views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("projects/", project_views.project_list, name="project_list"),
    path("tasks/", project_views.task_list, name="tasks"),
    path("kanban/", project_views.kanban_board, name="kanban"),
    path("reports/", views.reports, name="reports"),
    path("team-members/", views.team_members, name="team_members"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("organization/", views.organization, name="organization"),
]