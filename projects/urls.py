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

    path(
    'project/<int:project_id>/members/',
    views.get_project_members,
    name='project_members'
    ),


    # ================= TASK =================

   path('tasks/', views.task_list, name='tasks_list'),

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

    path('kanban/', views.kanban_board, name='kanban'),

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

# ================= NOTIFICATIONS =================

path(
    'notifications/',
    views.get_notifications,
    name='get_notifications'
),

path(
    'notifications/count/',
    views.notification_count,
    name='notification_count'
),

path(
    'notifications/read/<int:notification_id>/',
    views.mark_notification_read,
    name='mark_notification_read'
),
]