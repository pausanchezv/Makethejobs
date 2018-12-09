from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
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
        The register is being done when accessing via POST
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
        The register is being done when accessing via POST
        """
        context = {}

        # Checking the current password
        raw_password = self.request.POST.get('password0', '')

        if len(raw_password.strip()) < 1:
            context['error_password0'] = 'Password cannot be empty'

        else:

            user = authenticate(username=self.request.user.username, password=raw_password)

            if user is not None:

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


