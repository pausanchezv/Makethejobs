from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """ Customized Login Form"""

    email = forms.EmailField(label='Email', max_length=25, widget=forms.EmailInput(
        attrs={"placeholder": 'e.g. vincent@gmail.com'})
     )
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": 'e.g. asd567asdFG'})
    )

    def __init__(self, *args, **kwargs):
        """
        Change the default behavior
        """
        super(LoginForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



