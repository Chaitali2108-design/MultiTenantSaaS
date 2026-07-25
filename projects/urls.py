from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('tasks/', views.task_list, name='task_list'),

    path('create/', views.create_project, name='create_project'),
    path('tasks/create/', views.create_task, name='create_task'),
]