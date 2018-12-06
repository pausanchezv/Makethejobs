from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def base_redirect(request):
    """ Redirect to main page """
    return HttpResponse("Home. You're at the makethejobs index.")
