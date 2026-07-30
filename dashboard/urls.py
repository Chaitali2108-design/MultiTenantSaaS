from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("projects/", views.project_list, name="project_list"),
    path("tasks/", views.tasks, name="tasks"),
    path("kanban/", views.kanban, name="kanban"),
    path("reports/", views.reports, name="reports"),
    path("team-members/", views.team_members, name="team_members"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("organization/", views.organization, name="organization"),
]