from django.core.management.base import BaseCommand

from accounts.models import (
    PermissionGroup,
    Permission,
)


class Command(BaseCommand):

    help = "Create default system permissions"


    def handle(self, *args, **kwargs):

        permissions = {


            "Users": [

                ("View Users", "users.view"),
                ("Create Users", "users.create"),
                ("Update Users", "users.update"),
                ("Delete Users", "users.delete"),

            ],


            "Projects": [

                ("View Projects", "projects.view"),
                ("Create Projects", "projects.create"),
                ("Update Projects", "projects.update"),
                ("Delete Projects", "projects.delete"),

            ],


            "Tasks": [

                ("View Tasks", "tasks.view"),
                ("Create Tasks", "tasks.create"),
                ("Update Tasks", "tasks.update"),
                ("Delete Tasks", "tasks.delete"),

            ],


            "Reports": [

                ("View Reports", "reports.view"),
                ("Export Reports", "reports.export"),

            ],


            "Roles": [

                ("View Roles", "roles.view"),
                ("Create Roles", "roles.create"),
                ("Update Roles", "roles.update"),
                ("Delete Roles", "roles.delete"),

            ],

        }


        for group_name, permission_list in permissions.items():


            group, created = PermissionGroup.objects.get_or_create(
                name=group_name
            )


            for name, codename in permission_list:

                Permission.objects.get_or_create(
                    codename=codename,
                    defaults={
                        "name": name,
                        "group": group,
                    }
                )


        self.stdout.write(
            self.style.SUCCESS(
                "Default permissions created successfully"
            )
        )