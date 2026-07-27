from django.db import migrations


def assign_default_role_permissions(apps, schema_editor):

    Role = apps.get_model(
        "accounts",
        "Role",
    )

    Permission = apps.get_model(
        "accounts",
        "Permission",
    )


    role_permissions = {

        "Owner": [
            "view_project",
            "create_project",
            "update_project",
            "delete_project",

            "view_task",
            "create_task",
            "update_task",
            "delete_task",

            "view_user",
            "create_user",
            "update_user",
            "delete_user",

            "view_reports",

            "view_billing",
            "manage_subscription",
        ],


        "Admin": [
            "view_project",
            "create_project",
            "update_project",
            "delete_project",

            "view_task",
            "create_task",
            "update_task",
            "delete_task",

            "view_user",
            "create_user",
            "update_user",
            "delete_user",

            "view_reports",

            "view_billing",
        ],


        "Manager": [
            "view_project",
            "create_project",
            "update_project",

            "view_task",
            "create_task",
            "update_task",

            "view_reports",
        ],


        "Member": [
            "view_project",

            "view_task",
            "create_task",
            "update_task",
        ],


        "Viewer": [
            "view_project",

            "view_task",

            "view_reports",
        ],

    }


    for role_name, permission_codes in role_permissions.items():

        roles = Role.objects.filter(
            name=role_name,
            is_system=True,
        )


        for role in roles:

            permissions = Permission.objects.filter(
                codename__in=permission_codes
            )

            role.permissions.set(
                permissions
            )



def remove_role_permissions(apps, schema_editor):

    Role = apps.get_model(
        "accounts",
        "Role",
    )

    for role in Role.objects.filter(
        is_system=True
    ):

        role.permissions.clear()



class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0008_role_permissions",
        ),
    ]


    operations = [

        migrations.RunPython(
            assign_default_role_permissions,
            remove_role_permissions,
        ),

    ]
