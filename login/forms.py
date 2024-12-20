import re
import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction


User = get_user_model()
logger = logging.getLogger(__name__)

class LogInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data['username']
        if re.fullmatch(r'\w+@\w+\.\w\w+', username):
            user = User.objects.get(email=username)
            self.cleaned_data['username'] = user.username

        super().clean()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
    )
    email = forms.EmailField(
        max_length=254,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Email'}),
        error_messages={'unique': 'A user with that email already exists.'},
    )
    username = forms.CharField(
        max_length=150,
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'}),
        error_messages={'unique': 'A user with that username already exists.'},
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password confirmation'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
