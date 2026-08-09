from django.urls import path
from . import views

urlpatterns = [
    path("", views.reports, name="reports"),
    path("export/", views.export_report, name="export_report"),
]