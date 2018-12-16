
from django.http import HttpResponseRedirect
from django.urls import reverse
import re

from makethejobs.settings import PRIVATE_URLS_IF_LOGGED_IN, PRIVATE_URLS_IF_LOGGED_OUT


class LoginRedirectMiddleware(object):
    """ Login Redirections """

    def __init__(self, get_response):
        """ Middleware Constructor """
        self.get_response = get_response

    def __call__(self, request):
        """ Middleware callable """
        response = self.get_response(request)
        return response

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        """ Before accessing view functions """

        # Checking user session
        assert hasattr(request, 'user')
        is_session_active = request.user.is_authenticated

        # Getting the current path
        current_url = request.path_info.lstrip('/')

        # Compile URL(s)
        compiled_private_when_logged_in = map(lambda url: re.compile(url), PRIVATE_URLS_IF_LOGGED_IN)
        compiled_private_when_logged_out = map(lambda url: re.compile(url), PRIVATE_URLS_IF_LOGGED_OUT)

        # Getting the booleans
        is_private_when_logged_in = any(url.match(current_url) for url in compiled_private_when_logged_in)
        is_private_when_logged_out = any(url.match(current_url) for url in compiled_private_when_logged_out)

        # Redirect to userhome if users are not logged in
        if is_session_active and is_private_when_logged_in:
            return HttpResponseRedirect(reverse('profiles:userhome'))

        #TODO: it is not being used for now in order to take advantage of next sessions
        # Redirect to login if users are not logged in
        #elif not is_session_active and is_private_when_logged_out:
            #return HttpResponseRedirect(reverse('accounts:login'))

        return None
