from django.db import models
from django.conf import settings
from organizations.models import Organization
from django.utils import timezone


STATUS_CHOICES = [
    ('todo', 'To Do'),
    ('progress', 'In Progress'),
    ('done', 'Done'),
]

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    due_date = models.DateField(null=True, blank=True)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='project_members',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress(self):
        tasks = self.task_set.all()
        if not tasks.exists():
            return 0
        return int(sum([task.progress for task in tasks]) / tasks.count())

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    due_date = models.DateField(null=True, blank=True)

    reminder_date = models.DateTimeField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)

    dependency = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='dependent_tasks'
    )

    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress(self):
        if self.status == 'todo':
            return 0
        elif self.status == 'progress':
            return 50
        return 100

    @property
    def is_overdue(self):
        return self.due_date and self.status != 'done' and self.due_date < timezone.now().date()

    def __str__(self):
        return self.title


class ActivityLog(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"