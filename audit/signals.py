from django.db.models.signals import (
    post_save,
    post_delete,
    pre_save,
    pre_delete
)

from django.dispatch import receiver

from projects.models import Project, Task
from accounts.models import User, Role, Permission

from .utils import create_audit_log

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
)

from django.dispatch import receiver

#login audit
@receiver(user_logged_in)
def login_audit(
    sender,
    request,
    user,
    **kwargs
):

    create_audit_log(
        action="login",
        model_name="Authentication",
        object_id=user.id,
        description=(
            f"User logged in: "
            f"{user.username}"
        ),
    )

#logout audit
@receiver(user_logged_out)
def logout_audit(
    sender,
    request,
    user,
    **kwargs
):

    if user:

        create_audit_log(
            action="logout",
            model_name="Authentication",
            object_id=user.id,
            description=(
                f"User logged out: "
                f"{user.username}"
            ),
        )

# -----------------------------
# Project Audit
# -----------------------------

@receiver(post_save, sender=Project)
def project_audit(sender, instance, created, **kwargs):

    action = "create" if created else "update"

    create_audit_log(
        action=action,
        model_name="Project",
        object_id=instance.id,
        description=f"{action.capitalize()}d project: {instance.name}",
        project=instance,
    )

@receiver(pre_delete, sender=Project)
def project_delete_audit(sender, instance, **kwargs):
    create_audit_log(
        action="delete",
        model_name="Project",
        object_id=instance.id,
        description=f"Deleted project: {instance.name}",
        project=None,
    )

# -----------------------------
# Task Audit
# -----------------------------

@receiver(post_save, sender=Task)
def task_audit(sender, instance, created, **kwargs):

    action = "create" if created else "update"

    create_audit_log(
        action=action,
        model_name="Task",
        object_id=instance.id,
        description=f"{action.capitalize()}d task: {instance.title}",
        project=instance.project,
        task=instance,
    )


@receiver(pre_delete, sender=Task)
def task_delete_audit(sender, instance, **kwargs):

    create_audit_log(
        action="delete",
        model_name="Task",
        object_id=instance.id,
        description=f"Deleted task: {instance.title}",
        project=None,
        task=None,
    )

# -----------------------------
# User Audit
# -----------------------------

@receiver(pre_save, sender=User)
def user_audit(sender, instance, **kwargs):

    if not instance.pk:
        instance._role_changed = False
        return


    old_user = sender.objects.get(
        pk=instance.pk
    )


    old_role = (
        old_user.role.name
        if old_user.role
        else "None"
    )

    new_role = (
        instance.role.name
        if instance.role
        else "None"
    )


    if old_role != new_role:

        instance._role_changed = True

        instance._old_role = old_role
        instance._new_role = new_role

    else:

        instance._role_changed = False


@receiver(post_delete, sender=User)
def user_delete_audit(sender, instance, **kwargs):

    create_audit_log(
        action="delete",
        model_name="User",
        object_id=instance.id,
        description=f"Deleted user: {instance.username}",
    )

@receiver(post_save, sender=User)
def user_save_audit(sender, instance, created, **kwargs):

    if created:

        create_audit_log(
            action="create",
            model_name="User",
            object_id=instance.id,
            description=f"Created user: {instance.username}",
        )

        return


    if getattr(instance, "_role_changed", False):

        create_audit_log(
            action="permission",
            model_name="Role Assignment",
            object_id=instance.id,
            description=(
                f"Changed role of {instance.username} "
                f"from {instance._old_role} "
                f"to {instance._new_role}"
            ),
        )

    else:

        create_audit_log(
            action="update",
            model_name="User",
            object_id=instance.id,
            description=f"Updated user: {instance.username}",
        )

# -----------------------------
# Role Audit
# -----------------------------

@receiver(post_save, sender=Role)
def role_audit(sender, instance, created, **kwargs):

    action = "create" if created else "update"

    create_audit_log(
        action=action,
        model_name="Role",
        object_id=instance.id,
        description=f"{action.capitalize()}d role: {instance.name}",
    )


@receiver(post_delete, sender=Role)
def role_delete_audit(sender, instance, **kwargs):

    create_audit_log(
        action="delete",
        model_name="Role",
        object_id=instance.id,
        description=f"Deleted role: {instance.name}",
    )


# -----------------------------
# Permission Audit
# -----------------------------

@receiver(post_save, sender=Permission)
def permission_audit(sender, instance, created, **kwargs):

    action = "create" if created else "update"

    create_audit_log(
        action="permission",
        model_name="Permission",
        object_id=instance.id,
        description=f"{action.capitalize()}d permission: {instance.codename}",
    )


# -----------------------------
# User Role Change Audit
# -----------------------------

@receiver(pre_save, sender=User)
def user_role_change_audit(sender, instance, **kwargs):

    if not instance.pk:
        return


    old_user = sender.objects.get(
        pk=instance.pk
    )


    old_role = (
        old_user.role.name
        if old_user.role
        else "None"
    )


    new_role = (
        instance.role.name
        if instance.role
        else "None"
    )


    if old_role != new_role:

        create_audit_log(
            action="permission",
            model_name="Role Assignment",
            object_id=instance.id,
            description=(
                f"Changed role of {instance.username} "
                f"from {old_role} to {new_role}"
            ),
        )