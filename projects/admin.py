from django.contrib import admin
from .models import Project, Task


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_by')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'organization')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)