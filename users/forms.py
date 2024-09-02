from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name', 'groups', 'user_permissions', 'gender')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name', 'groups', 'user_permissions', 'gender')


class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()
        