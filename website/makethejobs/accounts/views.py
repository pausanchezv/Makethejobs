from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from accounts.forms import LoginForm


def home(request):
    #return HttpResponse("Hello, world. You're at the makethejobs index.")

    return render(request, 'accounts/login.html')


class Login(FormView):
    """ Login Customized View """

    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = 'accounts:home'

    def form_valid(self, form):
        return HttpResponseRedirect(reverse(Login.success_url))

    def form_invalid(self, form):
        a=2
