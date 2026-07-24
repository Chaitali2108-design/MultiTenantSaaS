from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User
from organizations.models import Organization


class OrganizationOwnerSignupForm(UserCreationForm):

    organization_name = forms.CharField(
        max_length=150
    )

    domain = forms.CharField(
        max_length=100,
        required=False
    )

    logo = forms.ImageField(
        required=False
    )

    plan = forms.ChoiceField(
        choices=Organization.PLAN_CHOICES
    )

    contact_email = forms.EmailField()

    contact_phone = forms.CharField(
        max_length=20,
        required=False
    )

    class Meta:
        model = User

        fields = [
            "organization_name",
            "domain",
            "logo",
            "plan",
            "contact_email",
            "contact_phone",
            "username",
            "email",
            "password1",
            "password2",
        ]

    @transaction.atomic
    def save(self, commit=True):

        organization = Organization.objects.create(
            name=self.cleaned_data["organization_name"],
            domain=self.cleaned_data["domain"],
            logo=self.cleaned_data.get("logo"),
            contact_email=self.cleaned_data["contact_email"],
            contact_phone=self.cleaned_data["contact_phone"],
            plan=self.cleaned_data["plan"],
        )

        user = super().save(commit=False)

        user.organization = organization
        user.role = "OWNER"

        if commit:
            user.save()

        return user