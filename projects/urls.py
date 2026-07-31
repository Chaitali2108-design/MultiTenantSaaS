from django.urls import path
from . import views


urlpatterns = [

    # ================= PROJECT =================

    path('', views.project_list, name='project_list'),

    path(
        'create/',
        views.create_project,
        name='create_project'
    ),

    path(
        'update/<int:project_id>/',
        views.update_project,
        name='update_project'
    ),

    path(
        'delete/<int:project_id>/',
        views.delete_project,
        name='delete_project'
    ),

    path(
        '<int:project_id>/',
        views.project_detail,
        name='project_detail'
    ),


    # ================= TASK =================

    path(
        'tasks/',
        views.task_list,
        name='task_list'
    ),

    path(
        'tasks/create/',
        views.create_task,
        name='create_task'
    ),

    path(
        'tasks/<int:task_id>/',
        views.task_detail,
        name='task_detail'
    ),

    path(
        'tasks/update/<int:task_id>/',
        views.update_task,
        name='update_task'
    ),

    path(
        'tasks/delete/<int:task_id>/',
        views.delete_task,
        name='delete_task'
    ),


    # ================= KANBAN =================

    path(
        'kanban/',
        views.kanban_board,
        name='kanban_board'
    ),

    path(
        'tasks/update-status/<int:task_id>/',
        views.update_task_status,
        name='update_task_status'
    ),


    # ================= EXPORT =================

    path(
        'tasks/export/csv/',
        views.export_tasks_csv,
        name='export_tasks_csv'
    ),

]