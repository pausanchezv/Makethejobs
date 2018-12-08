from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, RedirectView
from accounts.forms import LoginForm


class Login(FormView):
    """ Login Customized View """

    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = 'profiles:userhome'
    error_url = 'accounts:login'

    def _login(self, data):
        """
        Login with email
        :param data:
        :return: Response Redirect
        """

        email = data.get('email', '')
        password = data.get('password', '')

        user = authenticate(username=email, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(reverse(Login.success_url))

        return HttpResponseRedirect(reverse(Login.error_url) + '?errors=does-not-exist')

    def form_valid(self, form):
        """
        Actions when the form has been successfully filled
        :param form: login form
        :return: Response redirect from _login function
        """
        return self._login(form.cleaned_data)

    def form_invalid(self, form):
        """
        Actions when the form has been unsuccessfully filled
        :param form: login form
        :return: Response Redirect with errors
        """
        return HttpResponseRedirect(reverse(Login.error_url) + '?errors=form-error')


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
