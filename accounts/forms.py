from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs['class'] = 'form-input'


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs['class'] = 'form-input'

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
