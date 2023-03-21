import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from app_users.forms import AuthForm, RestorePasswordForm
import time

from django.urls import reverse
from django.views import View
from django.contrib.auth.views import LoginView
from app_users.forms import RegisterForm, EditProfileForm
from django.views.generic import ListView, DetailView

from app_users.models import Profile


def login_view(request):
    if request.method == 'POST':    #для POST пытаемся аутентифицировать пользователя
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_superuser:
                    auth_form.add_error('__all__', 'Вход администаторам не здесь!')
                elif user.is_active:
                    login(request, user)
                    return HttpResponse('Вы успешно вошли в систему')

            else:
                auth_form.add_error('__all__', 'Ошибка! Проверьте правильность написания логина и пароля')

    else:   # для всех остальных запросов просто отображаем саму страничку логина
        auth_form = AuthForm()
    context = {
        'form': auth_form
    }
    return render(request, 'app_users/login.html', context=context)


class AnotherLoginView(LoginView):
    template_name = 'app_users/login.html'

def logout_view(request):
    logout(request)
    return HttpResponse('Вы успешно вышли из учетной записи')

class AnotherLogoutView(LogoutView):
    #template_name = 'app_users/another_logout.html'
    next_page = '/'


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'app_users/register.html', {'form': form})

def another_register_view(request):
    """регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            date_of_birth = form.cleaned_data.get('date_of_birth')
            city = form.cleaned_data.get('city')
            phone_number = form.cleaned_data.get('phone_number')
            sale_card = form.cleaned_data.get('sale_card')
            Profile.objects.create(user=user,
                                   city=city,
                                   phone_number=phone_number,
                                   date_of_birth=date_of_birth,
                                   sale_card=sale_card)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if request.user.is_authenticated:
                login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', {'form': form})

def account(request):
    '''страница инфо профиля'''
    user = request.user
    return render(request, 'app_users/account.html', {'user': user})

def edit_account(request):
    """редактирует данные из модели Profile"""
    user = User.objects.get(username=request.user)
    profile = user.profile
    form = EditProfileForm(instance=profile)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = user
            update.save()
        return HttpResponseRedirect(reverse('account'))
    else:
        form = EditProfileForm(instance=profile)
    return render(request, "app_users/edit_profile.html", {'form': form})


def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            new_password = User.objects.make_random_password()
            current_user = User.objects.filter(email=user_email).first()
            if current_user:
                current_user.set_password(new_password)
                current_user.save()
            send_mail(
                subject='Восстановление пароля',
                message='Test',
                from_email='admin@company.com',
                recipient_list=[form.cleaned_data['email']]
            )
            return HttpResponse('Письмо отправлено')
    restore_password_form = RestorePasswordForm()
    context = {
        'form': restore_password_form
    }
    return render(request, 'app_users/restore_password.html', context=context)

