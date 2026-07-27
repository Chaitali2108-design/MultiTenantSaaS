from django.db import migrations


def create_default_permissions(apps, schema_editor):

    PermissionGroup = apps.get_model(
        "accounts",
        "PermissionGroup",
    )

    Permission = apps.get_model(
        "accounts",
        "Permission",
    )


    permissions = {

        "Projects": [
            ("View Project", "view_project"),
            ("Create Project", "create_project"),
            ("Update Project", "update_project"),
            ("Delete Project", "delete_project"),
        ],


        "Tasks": [
            ("View Task", "view_task"),
            ("Create Task", "create_task"),
            ("Update Task", "update_task"),
            ("Delete Task", "delete_task"),
        ],


        "Users": [
            ("View User", "view_user"),
            ("Create User", "create_user"),
            ("Update User", "update_user"),
            ("Delete User", "delete_user"),
        ],


        "Reports": [
            ("View Reports", "view_reports"),
        ],


        "Billing": [
            ("View Billing", "view_billing"),
            ("Manage Subscription", "manage_subscription"),
        ],

    }


    for group_name, permission_list in permissions.items():

        group, created = PermissionGroup.objects.get_or_create(
            name=group_name,
        )


        for permission_name, codename in permission_list:

            Permission.objects.get_or_create(
                group=group,
                name=permission_name,
                codename=codename,
            )



def remove_default_permissions(apps, schema_editor):

    PermissionGroup = apps.get_model(
        "accounts",
        "PermissionGroup",
    )

    PermissionGroup.objects.filter(
        name__in=[
            "Projects",
            "Tasks",
            "Users",
            "Reports",
            "Billing",
        ]
    ).delete()



class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_permissiongroup_permission"),
    ]


    operations = [

        migrations.RunPython(
            create_default_permissions,
            remove_default_permissions,
        ),

    ]