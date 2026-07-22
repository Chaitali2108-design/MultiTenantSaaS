from django import forms
from .models import Organization

class OrganizationRegistrationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            "name",
            "domain",
            "logo",
            "contact_email",
            "contact_phone",
            "plan",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Organization Name",
            }),
            "domain": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "company",
            }),
            "contact_email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "admin@example.com",
            }),
            "contact_phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+91XXXXXXXXXX",
            }),
            "plan": forms.Select(attrs={
                "class": "form-select",
            }),
            "logo": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }