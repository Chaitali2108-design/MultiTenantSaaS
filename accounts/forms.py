from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Role, User
from organizations.models import Organization
from .models import UserProfile
from .models import UserInvitation




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






class UserInvitationForm(forms.ModelForm):

    class Meta:
        model = UserInvitation
        fields = ["email", "role"]

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-green-500",
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "w-full bg-[#1E1630] text-white border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-green-500 appearance-none",
                }
            ),
        }


    def __init__(self, *args, **kwargs):

        organization = kwargs.pop(
            "organization",
            None
        )

        super().__init__(
            *args,
            **kwargs
        )


        if organization:

            self.fields["role"].queryset = Role.objects.filter(
                organization=organization
            )

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AcceptInvitationForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full",
                "placeholder": "Password",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full",
                "placeholder": "Confirm Password",
            }
        )
    )

    class Meta:

        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
        )

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data