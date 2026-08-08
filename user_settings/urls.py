from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.settings_page,
        name="user_settings"
    ),

]