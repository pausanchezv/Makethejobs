from django.core.mail import EmailMessage
from django.template.loader import get_template

from accounts.models import User
from makethejobs.settings import WEBSITE_EMAILS


class EmailManager(object):
    """ Email Manager"""

    # Email templates
    REGISTER_EMAIL_TEMPLATE = 'accounts/email_templates/register_email.html'
    RECOVER_PASSWORD_EMAIL_TEMPLATE = 'accounts/email_templates/password_email.html'

    @classmethod
    def send_email(cls, subject: str, message: str, to: list, from_email: str) -> None:
        """
        Generic email sender
        :param subject: The headline of the email
        :param message: Email body
        :param to: User email(s) which the message is sent to
        :param from_email: Platform email sending the message
        :return: None
        """
        email = EmailMessage(subject, message, to=to, from_email=from_email)
        email.content_subtype = 'html'
        email.send()

    @staticmethod
    def register_email(user: User) -> None:
        """
        Email sent when a new user is registered
        :param user: models.User
        :return: None
        """

        context = {
            'user': user,
        }

        # Preparing the email
        subject = "Welcome to Makethejobs"
        to = [user.email]
        from_email = WEBSITE_EMAILS['general']
        message = get_template(__class__.REGISTER_EMAIL_TEMPLATE).render(context)

        # Sending the email
        __class__.send_email(subject, message, to, from_email)

    @staticmethod
    def password_email(user: User, link: str) -> None:
        """
        Email sent when a new user is registered
        :param link: str
        :param user: models.User
        :return: None
        """

        context = {
            'user': user,
            'link': link
        }

        # Preparing the email
        subject = "Makethejobs password recovery"
        to = [user.email]
        from_email = WEBSITE_EMAILS['general']
        message = get_template(__class__.RECOVER_PASSWORD_EMAIL_TEMPLATE).render(context)

        # Sending the email
        __class__.send_email(subject, message, to, from_email)
