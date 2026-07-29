from django.urls import path

from . import views


app_name = "audit"


urlpatterns = [

    path(
        "activity-report/",
        views.activity_report,
        name="activity_report",
    ),

]