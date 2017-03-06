from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms import ValidationError

class LoginForm(AuthenticationForm):
    """
    Basic form for our user login view
    """
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class InitialLogin(forms.Form):
    """
    Form for the initial login information request view. Here the user
    should enter all required information about themselves.
    """

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(InitialLogin, self).__init__(*args, **kwargs)

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100, label='Your e-mail address')
    old_password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput(), label='New password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Re-enter password')

    def clean(self):

        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        old_password=self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise ValidationError('Current password incorrect.')

        if password1 and password1 != password2 :
            raise ValidationError('Re-entered password does not match the new password.')

        if password1 == old_password:
            raise ValidationError('New password cannot be the same as the current password.')

        return self.cleaned_data
