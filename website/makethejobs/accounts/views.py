from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, RedirectView
from accounts.forms import LoginForm, RegistrationForm


class Login(FormView):
    """ Login Customized View """

    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = 'profiles:userhome'
    error_url = 'accounts:login'

    def form_valid(self, form, *args, **kwargs):
        """
        Actions when the form has been successfully filled
        :param form: login form
        :return: Response redirect from _login function
        """
        email = form.data.get('email', '')
        password = form.data.get('password', '')

        user = authenticate(username=email, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(reverse(Login.success_url))

        # Getting the context from the superclass
        context = super(Login, self).get_context_data(**kwargs)
        context['invalid_credentials'] = 'Invalid login credentials'

        return render(self.request, Login.template_name, context)

    def form_invalid(self, form, *args, **kwargs):
        """
        Actions when the form has been unsuccessfully filled
        :param form: login form
        :return: Response Redirect with errors
        """
        if form.data.get('email', '') == '' and form.data.get('password', '') != '':
            return HttpResponseRedirect(reverse(Login.error_url) + '?errors=email')

        if form.data.get('email', '') != '' and form.data.get('password', '') == '':
            return HttpResponseRedirect(reverse(Login.error_url) + '?errors=password')

        return HttpResponseRedirect(reverse(Login.error_url) + '?errors=all')


class Logout(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        """
        Get method for RedirectView Class
        :param request:
        :return: Super call
        """
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class Register(FormView):
    """ Login Customized View """

    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = 'profiles:userhome'
    error_url = 'accounts:register'

    def form_valid(self, form, *args, **kwargs):
        """
        Actions when the form has been successfully filled
        :param form: login form
        :return: Response redirect from _login function
        """
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        return HttpResponseRedirect(reverse(Register.success_url))

    def form_invalid(self, form, *args, **kwargs):
        """
        Actions when the form has been unsuccessfully filled
        :param form: login form
        :return: Response Redirect with errors
        """

        return HttpResponseRedirect(reverse(Register.error_url) + '?errors')