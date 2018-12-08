from django.contrib.auth import backends

from accounts.models import User


class EmailAuthBackend(backends.ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair, then check
    a username/password pair if email failed
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on email address as the user name
        :param request: current request object
        :param username: user's email/username
        :param password: user's password
        :return: User
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        """
        Get a User object from the user_id
        :param user_id: user pk
        :return: User or None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
