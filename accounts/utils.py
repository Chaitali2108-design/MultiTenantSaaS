from .models import Role


def assign_default_permissions(role):
    """
    Assign Member permissions to newly created custom roles.
    """

    try:
        member_role = Role.objects.get(
            organization=role.organization,
            name="Member",
        )

        role.permissions.set(
            member_role.permissions.all()
        )

    except Role.DoesNotExist:
        pass

from django.core.mail import send_mail
from django.conf import settings



def send_invitation_email(invitation, invitation_url):


    subject = "Invitation to join MultiTenant SaaS"


    message = f"""
Hello,

You have been invited to join:

Organization:
{invitation.organization.name}


Assigned Role:
{invitation.role.name if invitation.role else "Member"}


Click the link below to create your account:

{invitation_url}


This invitation link is secure and can only be used once.


Thank you,
MultiTenant SaaS Team
"""


    send_mail(

        subject,

        message,

        settings.EMAIL_HOST_USER,

        [invitation.email],

        fail_silently=False

    )