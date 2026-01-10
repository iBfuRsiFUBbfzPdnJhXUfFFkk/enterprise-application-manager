from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    """
    Custom login form that adds autocomplete attributes for better UX.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add autocomplete attribute to username field
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
        })

        # Add autocomplete attribute to password field
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
        })
