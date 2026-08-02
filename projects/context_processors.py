from django.utils import timezone
from .models import Task


def reminders(request):

    if not request.user.is_authenticated:
        return {}

    tasks = Task.objects.filter(
        reminder_date__lte=timezone.now(),
        reminder_sent=False,
        organization=request.user.organization
    )

    reminder_messages = []

    for task in tasks:

        if task.priority == "high":
            reminder_messages.append(
                f"🚨 HIGH PRIORITY Reminder: {task.title}"
            )

        elif task.priority == "medium":
            reminder_messages.append(
                f"⚠️ Reminder: {task.title}"
            )

        else:
            reminder_messages.append(
                f"🔔 Reminder: {task.title}"
            )

        task.reminder_sent = True
        task.save()

    return {
        "reminder_messages": reminder_messages
    }