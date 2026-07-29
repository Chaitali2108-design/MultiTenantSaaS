from django.db import models
from accounts.models import User
from organizations.models import Organization


# PROJECT MODEL
class Project(models.Model):

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # AUTOMATIC PROJECT PROGRESS
    @property
    def progress(self):

        tasks = self.task_set.all()

        total_tasks = tasks.count()


        if total_tasks == 0:
            return 0


        total_progress = 0


        for task in tasks:

            if task.status == "todo":
                total_progress += 0

            elif task.status == "progress":
                total_progress += 50

            elif task.status == "done":
                total_progress += 100


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





# TASK MODEL
class Task(models.Model):

    title = models.CharField(
        max_length=255
    )


    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )


    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )


    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


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


    created_at = models.DateTimeField(
        auto_now_add=True
    )



    # AUTOMATIC TASK PROGRESS
    @property
    def progress(self):

        if self.status == "todo":
            return 0

        elif self.status == "progress":
            return 50

        elif self.status == "done":
            return 100

        return 0



    def __str__(self):

        return self.title