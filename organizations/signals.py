from django.db.models.signals import post_save
from django.dispatch import receiver

from organizations.models import Organization
from accounts.models import Role, Permission



@receiver(post_save, sender=Organization)
def create_default_roles(sender, instance, created, **kwargs):

    if not created:
        return


    all_permissions = Permission.objects.all()


    # Owner - Full access

    owner = Role.objects.create(
        organization=instance,
        name="Owner",
        description="Organization owner with full access.",
        is_system=True,
        is_editable=False,
    )

    owner.permissions.set(
        all_permissions
    )


    # Admin

    admin = Role.objects.create(
        organization=instance,
        name="Admin",
        description="Administrator with management access.",
        is_system=True,
        is_editable=False,
    )


    # Manager

    manager = Role.objects.create(
        organization=instance,
        name="Manager",
        description="Manager with team and project access.",
        is_system=True,
        is_editable=False,
    )


    management_permissions = Permission.objects.filter(
        codename__in=[

            "users.view",
            "users.create",
            "users.update",

            "projects.view",
            "projects.create",
            "projects.update",

            "tasks.view",
            "tasks.create",
            "tasks.update",

            "reports.view",

            "roles.view",

        ]
    )


    admin.permissions.set(
        management_permissions
    )


    manager.permissions.set(
        management_permissions
    )


    # Member

    member = Role.objects.create(
        organization=instance,
        name="Member",
        description="Basic organization member.",
        is_system=True,
        is_editable=False,
    )


    # Viewer

    viewer = Role.objects.create(
        organization=instance,
        name="Viewer",
        description="Read only access.",
        is_system=True,
        is_editable=False,
    )


    basic_permissions = Permission.objects.filter(
        codename__in=[

            "users.view",

            "projects.view",

            "tasks.view",

            "roles.view",

        ]
    )


    member.permissions.set(
        basic_permissions
    )


    viewer.permissions.set(
        basic_permissions
    )