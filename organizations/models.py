from django.db import models

from organizations.utils import PLAN_LIMITS


class Organization(models.Model):
    """
    Represents a tenant (organization/company) in the SaaS platform.
    Every user belongs to one organization.
    """

    PLAN_CHOICES = [
        ("FREE", "Free"),
        ("BASIC", "Basic"),
        ("PRO", "Pro"),
        ("ENTERPRISE", "Enterprise"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    name = models.CharField(max_length=150, unique=True)
    domain = models.CharField(max_length=100, unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to="organization_logos/", blank=True, null=True)

    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="FREE",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    max_users = models.PositiveIntegerField(default=5)
    max_projects = models.PositiveIntegerField(default=5)
    storage_limit_gb = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        from .utils import PLAN_LIMITS

        limits = PLAN_LIMITS.get(self.plan)

        if limits:
            self.max_users = limits["max_users"]
            self.max_projects = limits["max_projects"]
            self.storage_limit_gb = limits["storage_limit_gb"]

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name