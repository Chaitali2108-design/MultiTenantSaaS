from django.db.models.signals import post_save
from django.dispatch import receiver

from organizations.models import Organization
from accounts.models import Role


@receiver(post_save, sender=Organization)
def create_default_roles(sender, instance, created, **kwargs):

    if created:

        default_roles = [
            {
                "name": "Owner",
                "description": "Organization owner with full access.",
            },
            {
                "name": "Admin",
                "description": "Administrator with management access.",
            },
            {
                "name": "Manager",
                "description": "Can manage projects and team activities.",
            },
            {
                "name": "Member",
                "description": "Can work on assigned tasks and projects.",
            },
            {
                "name": "Viewer",
                "description": "Read-only access.",
            },
        ]

        for role in default_roles:

            Role.objects.create(
                organization=instance,
                name=role["name"],
                description=role["description"],
                is_system=True,
            )