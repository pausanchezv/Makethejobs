import random
import string

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView
from accounts.models import User


class CustomAuth(View):
    """ Customized Authentication Class """

    @staticmethod
    def check_username(username: str, context: dict):
        """
        Check whether the username is valid
        :param username: str
        :param context: dict
        :return: str | bool
        """
        username = username.strip()

        if username == '':
            context['error_username'] = 'Username cannot be empty'
            return False

        elif username[0].isnumeric():
            context['error_username'] = 'Username cannot start with a number'
            return False

        elif username.isalnum():

            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            else:
                context['error_username'] = 'This username already exists'
                return False

        context['error_username'] = 'Only letters and numbers without blank spaces'
        return False

    @staticmethod
    def check_email(email: str, context: dict):
        """
        Check whether teh email is valid
        :param email: str
        :param context: dict
        :return: str | bool
        """
        email = email.strip()

        if email == '':
            context['error_email'] = 'Email cannot be empty'
            return False

        try:
            validate_email(email)

        except ValidationError:
            context['error_email'] = 'This is not an email'
            return False

        else:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            else:
                context['error_email'] = 'This email already exists'

        return False

    @staticmethod
    def check_password(password1: str, password2: str, context: dict):
        """
        Check whether the passwords are ok
        :param password1: str
        :param password2: str
        :param context: dict
        :return: str | bool
        """
        password1 = password1.strip()

        if len(password1) < 1:
            context['error_password1'] = 'Password cannot be empty'
            return False

        if len(password1) < 6:
            context['error_password1'] = 'Password should have at least 6 characters'
            return False

        if password1 != password2:
            context['error_password2'] = 'These passwords are not equals'
            return False

        return password1


class Login(CustomAuth):
    """ Custom registration """

    template_name = 'accounts/login.html'
    success_url = 'profiles:userhome'

    def get(self, request, *args, **kwargs):
        """
        Return template render when accessing via GET
        """
        return render(self.request, Login.template_name)

    def post(self, request, *args, **kwargs):
        """
        The use is logged in when accessing via POST
        """
        context = {}

        username = self.request.POST.get('username', '')
        password = self.request.POST.get('password', '')

        # Authenticate and log in the user
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(reverse(Login.success_url))

        context['login_error'] = 'These login credentials are not valid'

        return render(self.request, Login.template_name, context)


class Register(CustomAuth):
    """ Custom registration """

    template_name = 'accounts/register.html'
    success_url = 'profiles:userhome'

    def get(self, request, *args, **kwargs):
        """
        Return template render when accessing via GET
        """
        return render(self.request, Register.template_name)

    def post(self, request, *args, **kwargs):
        """
        The register is being done when accessing via POST
        """
        context = {}

        # Checking the values
        username = super().check_username(self.request.POST.get('username', ''), context)
        email = super().check_email(self.request.POST.get('email', ''), context)
        raw_password = super().check_password(
            self.request.POST.get('password1', ''),
            self.request.POST.get('password2', ''),
            context
        )

        # Register if there are no errors
        if username and email and raw_password:
            return self.register(username, email, raw_password)

        return render(self.request, Register.template_name, context)

    def register(self, username: str, email: str, password: str):
        """
        Manual register system
        :param username: string
        :param email: string
        :param password: string
        :return: Redirect after logging in
        """

        # Create and save the new user
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        # Authenticate and log in the user
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return HttpResponseRedirect(reverse(Register.success_url))


class Logout(RedirectView):
    """ Provides users the ability to logout """

    url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Get method for RedirectView Class
        :param request:
        :return: Super call
        """
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class ChangePassword(CustomAuth):
    """ Custom ChangePassword Class"""

    template_name = 'accounts/change_password.html'
    success_url = 'profiles:userhome'

    def get(self, request, *args, **kwargs):
        """
        Return template render when accessing via GET
        """
        return render(self.request, ChangePassword.template_name)

    def post(self, request, *args, **kwargs):
        """
        The password is changed when accessing via POST
        """
        context = {}

        # Checking the current password
        raw_password = self.request.POST.get('password0', '')

        # Checking whether the password has length
        if len(raw_password.strip()) < 1:
            context['error_password0'] = 'Password cannot be empty'

        else:

            # Checking current password
            user = authenticate(username=self.request.user.username, password=raw_password)

            # Actions id the password is ok
            if user is not None:

                # New password validation
                raw_password = super().check_password(
                    self.request.POST.get('password1', ''),
                    self.request.POST.get('password2', ''),
                    context
                )

                # Change password if there are no errors
                if raw_password:
                    user.set_password(raw_password)
                    user.save()
                    return HttpResponseRedirect(reverse(ChangePassword.success_url) + '?password-changed=1')

            else:
                context['error_password0'] = 'Incorrect current password'

        return render(self.request, ChangePassword.template_name, context)


class ResetPassword(CustomAuth):
    """ Custom ChangePassword Class"""

    template_name = 'accounts/reset_password.html'
    success_url = 'accounts:login'
    TOKEN_LENGTH = 16

    def get(self, request, *args, **kwargs):
        """
        Receiving tokens via GET
        """

        # Get tokens
        try:
            needle = int(self.request.GET.get('needle', '')[::-1])
        except ValueError:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        label = self.request.GET.get('label', '')[::-1]
        key = self.request.GET.get('key', '')[::-1]
        public_token = self.request.GET.get('public_token', '')

        # Not found is the are token errors
        if len(public_token) != ResetPassword.TOKEN_LENGTH or not key:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        # Checking valid user
        try:
            User.objects.get(pk=needle, username=label)
        except User.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return render(self.request, ResetPassword.template_name)

    def post(self, request, *args, **kwargs):
        """
        Reset password via POST
        """
        context = {}

        # Checking the password
        raw_password = super().check_password(
            self.request.POST.get('password1', ''),
            self.request.POST.get('password2', ''),
            context
        )

        # New password validation
        if raw_password:

            reversed_key = self.request.POST.get('key', '')

            try:
                user = User.objects.get(email=reversed_key[::-1])

            except User.DoesNotExist:
                return HttpResponseNotFound('<h1>Page not found</h1>')

            else:
                user.set_password(raw_password)
                user.save()
                return HttpResponseRedirect(reverse(ResetPassword.success_url) + '?password-changed=1')

        # Always not found by default
        return render(self.request, ResetPassword.template_name, context)


class ForgottenPassword(CustomAuth):
    """ Custom ChangePassword Class"""

    template_name = 'accounts/forgotten_password.html'
    success_url = 'accounts:login'
    TOKEN_LENGTH = 16

    def get(self, request, *args, **kwargs):
        """
        Return template render when accessing via GET
        """
        return render(self.request, ForgottenPassword.template_name)

    def post(self, request, *args, **kwargs):
        """
        Sending the tokenized link
        """
        context = {}

        # Checking the email
        email = str(self.request.POST.get('email', '')).strip()

        if email:

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                context['error_email'] = 'This email does not exist'

            else:
                self.send_password_link(user)
                return HttpResponseRedirect(reverse(ForgottenPassword.success_url) + '?password-link-sent=1')

        return render(self.request, ForgottenPassword.template_name, context)

    @staticmethod
    def send_password_link(user):
        """
        Prepare and send a tokenized link
        :param user:
        :return:
        """
        public_token = (''.join(random.choice(string.ascii_letters + string.digits)
                                for _ in range(ForgottenPassword.TOKEN_LENGTH)))

        key = user.email[::-1]
        label = user.username[::-1]
        needle = str(user.pk)[::-1]

        link = reverse('accounts:reset_password') + '?key={}&label={}&needle={}&public_token={}'.format(
            key, label, needle, public_token
        )

        send_mail(
            'Makethejobs password recovery',
            'Link: {}'.format(link),
            'info@pausanchezv.com',
            (user.email,)
        )
















