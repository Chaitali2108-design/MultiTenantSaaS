from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list),
    path('create/', views.create_project),

    path('tasks/', views.task_list),
    path('tasks/create/', views.create_task),

    path('tasks/update/<int:task_id>/', views.update_task_status),

    path('<int:project_id>/', views.project_detail),

    path('kanban/', views.kanban_board),

    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]
