from django.db import models
from accounts.models import User
from organizations.models import Organization
from django.utils import timezone


class Project(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress(self):
        tasks = self.task_set.all()
        total_tasks = tasks.count()

        if total_tasks == 0:
            return 0

        total_progress = 0

        for task in tasks:
            total_progress += task.progress

        return int(total_progress / total_tasks)

    def __str__(self):
        return self.name


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


class Task(models.Model):

    title = models.CharField(max_length=255)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress(self):
        if self.status == "todo":
            return 0
        elif self.status == "progress":
            return 50
        elif self.status == "done":
            return 100
        return 0

    @property
    def is_overdue(self):
        if self.due_date and self.status != "done":
            return self.due_date < timezone.now().date()
        return False

    def __str__(self):
        return self.title