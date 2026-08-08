from django import forms

from .models import UserSetting


class UserSettingForm(forms.ModelForm):

    class Meta:
        model = UserSetting

        fields = [
            "email_notifications",
            "task_notifications",
            "project_notifications",
            "activity_notifications",
            "compact_mode",
            "show_completed_tasks",
        ]

        widgets = {
            field: forms.CheckboxInput(
                attrs={
                    "class": (
                        "h-5 w-5 rounded-lg "
                        "border-slate-300 "
                        "text-[#069494] "
                        "focus:ring-[#069494]/20"
                    )
                }
            )
            for field in [
                "email_notifications",
                "task_notifications",
                "project_notifications",
                "activity_notifications",
                "compact_mode",
                "show_completed_tasks",
            ]
        }