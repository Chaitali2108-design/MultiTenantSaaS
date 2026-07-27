from django.contrib.auth.models import AbstractUser
from django.db import models
from organizations.models import Organization

class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    

    role = models.ForeignKey(
    "Role",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="users",
)

    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.username


from django.db import models
from organizations.models import Organization


class Role(models.Model):

    name = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    permissions = models.ManyToManyField(
        "Permission",
        blank=True,
        related_name="roles",
    )

    is_system = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],
                name="unique_role_per_organization",
            )
        ]


    def __str__(self):
        return f"{self.organization.name} - {self.name}"


class PermissionGroup(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Permission(models.Model):

    name = models.CharField(
        max_length=100,
    )

    codename = models.CharField(
        max_length=100,
        unique=True,
    )

    group = models.ForeignKey(
        PermissionGroup,
        on_delete=models.CASCADE,
        related_name="permissions",
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["group", "name"]

    def __str__(self):
        return self.name