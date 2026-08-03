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

                "class":
                "w-full rounded-2xl border border-slate-300 "
                "bg-slate-50 px-4 py-3 text-slate-800 "
                "placeholder:text-slate-400 "
                "focus:outline-none focus:bg-white "
                "focus:border-cyan-500 "
                "focus:ring-4 focus:ring-cyan-100 "
                "transition duration-300",

                "placeholder":
                "Organization Name",

            }),



            "domain": forms.TextInput(attrs={

                "class":
                "w-full rounded-2xl border border-slate-300 "
                "bg-slate-50 px-4 py-3 text-slate-800 "
                "placeholder:text-slate-400 "
                "focus:outline-none focus:bg-white "
                "focus:border-cyan-500 "
                "focus:ring-4 focus:ring-cyan-100 "
                "transition duration-300",

                "placeholder":
                "company",

            }),



            "contact_email": forms.EmailInput(attrs={

                "class":
                "w-full rounded-2xl border border-slate-300 "
                "bg-slate-50 px-4 py-3 text-slate-800 "
                "placeholder:text-slate-400 "
                "focus:outline-none focus:bg-white "
                "focus:border-cyan-500 "
                "focus:ring-4 focus:ring-cyan-100 "
                "transition duration-300",

                "placeholder":
                "admin@example.com",

            }),



            "contact_phone": forms.TextInput(attrs={

                "class":
                "w-full rounded-2xl border border-slate-300 "
                "bg-slate-50 px-4 py-3 text-slate-800 "
                "placeholder:text-slate-400 "
                "focus:outline-none focus:bg-white "
                "focus:border-cyan-500 "
                "focus:ring-4 focus:ring-cyan-100 "
                "transition duration-300",

                "placeholder":
                "+91XXXXXXXXXX",

            }),



            "plan": forms.Select(attrs={

                "class":
                "w-full rounded-2xl border border-slate-300 "
                "bg-slate-50 px-4 py-3 text-slate-800 "
                "focus:outline-none focus:bg-white "
                "focus:border-cyan-500 "
                "focus:ring-4 focus:ring-cyan-100 "
                "transition duration-300",

            }),



            "logo": forms.FileInput(attrs={

                "class":
                "block w-full rounded-2xl border border-slate-300 "
                "bg-white p-3 text-slate-700 "
                "file:mr-4 file:rounded-xl "
                "file:border-0 "
                "file:bg-cyan-600 "
                "file:px-4 "
                "file:py-2 "
                "file:text-white "
                "hover:file:bg-cyan-700",

            }),

        }