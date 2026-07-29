from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Role, User
from organizations.models import Organization
from .models import UserProfile



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
        owner_role = Role.objects.get(
            organization=organization,
            name="Owner"
        )
        user.role = owner_role

        if commit:
            user.save()

        return user



class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = [
            "name",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Role Name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Description",
                }
            ),
        }




class UserRoleForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "role",
        ]

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)

        if organization:
            self.fields["role"].queryset = Role.objects.filter(
                organization=organization
            )

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

class ProfilePictureForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            "profile_picture",
        ]

class AccountSettingsForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            "timezone",
            "language",
            "theme",
            "email_notifications",
        ]