from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList

from accounts.models import User


# In form.py

from django.utils.safestring import mark_safe


class ErrorListMsg(ErrorList):
    def __unicode__(self):
        return self.as_msg()

    def as_msg(self):
        if not self:
            return u''
        return mark_safe(u'\n'.join([u'<span class="red">%s</span>' % e for e in self]))


class LoginForm(forms.Form):
    """ Customized Login Form"""

    email = forms.CharField(label='Email / Username', max_length=60, widget=forms.EmailInput(
        attrs={"placeholder": 'Type your email or username'})
     )
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": 'Type your password'})
    )

    def __init__(self, *args, **kwargs):
        """
        Change the default behavior
        """
        super(LoginForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RegistrationForm(UserCreationForm):
    """ Custom Register form """

    username = forms.CharField(label='Username', max_length=25, min_length=2, widget=forms.TextInput(
        attrs={"placeholder": 'Your username'})
    )

    '''first_name = forms.CharField(label='First Name', max_length=25, min_length=2, widget=forms.TextInput(
        attrs={"placeholder": 'Your first name'})
    )

    last_name = forms.CharField(label='Last Name', max_length=25, min_length=2, widget=forms.TextInput(
        attrs={"placeholder": 'Your last name'})
    )'''

    email = forms.CharField(label='Email', max_length=60, widget=forms.EmailInput(
        attrs={"placeholder": 'Your email'})
    )

    password1 = forms.CharField(label='Password', min_length=6, widget=forms.PasswordInput(
        attrs={"placeholder": 'Your password'})
    )

    password2 = forms.CharField(label='Password Confirmation', min_length=6, widget=forms.PasswordInput(
        attrs={"placeholder": 'Your password again'})
    )

    def __init__(self, *args, **kwargs):
        """
        Change the default behavior
        """
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        """ Meta Form """

        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        """ Save new user """

        user = super(RegistrationForm, self).save(commit=False)

        if commit:
            user.save()

        return user
