from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Profile


class AuthForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

class UpBalanceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['balance']
