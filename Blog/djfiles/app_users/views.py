from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from app_users.forms import AuthForm
import time
from django.urls import reverse
from django.views import View
from django.contrib.auth.views import LoginView
from app_users.forms import RegisterForm, EditProfileForm
from django.views.generic import ListView, DetailView
from app_users.models import Profile


class AnotherLoginView(LoginView):
    template_name = 'app_users/login.html'


class AnotherLogoutView(LogoutView):
    #template_name = 'app_users/another_logout.html'
    next_page = '/'


def another_register_view(request):
    """регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            date_of_birth = form.cleaned_data.get('date_of_birth')
            city = form.cleaned_data.get('city')
            phone_number = form.cleaned_data.get('phone_number')
            Profile.objects.create(user=user,
                                   city=city,
                                   phone_number=phone_number,
                                   date_of_birth=date_of_birth,
                                   )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', {'form': form})


def edit_account(request):
    """редактирует данные из модели Profile"""
    user = User.objects.get(username=request.user)
    profile = user.profile
    form = EditProfileForm(instance=profile)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = user
            update.save()
        return HttpResponseRedirect(reverse('account'))
    else:
        form = EditProfileForm(instance=user)
    return render(request, "app_users/edit_account.html", {'form': form})
