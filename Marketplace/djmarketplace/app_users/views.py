import datetime
import logging
from time import asctime

import self as self
from django.conf import settings
from django.shortcuts import render, resolve_url
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from app_users.forms import AuthForm
import time
from django.contrib import auth
from django.urls import reverse
from django.views import View
from django.contrib.auth.views import LoginView
from app_users.forms import RegisterForm, UpBalanceForm
from django.views.generic import ListView, DetailView
from app_users.models import Profile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app_orders.models import Order, OrderItem
from app_shop.models import Product
from django.core.cache import cache
logger = logging.getLogger(__name__)

def account(request):
    '''страница инфо профиля'''
    user = request.user
    user_orders = Order.objects.filter(user=request.user)
    user_order_item = OrderItem.objects.all()
    offers = Product.objects.order_by('price')[:2]
    offers_cache_key = 'offers:{}'.format(user)
    cache.get_or_set(offers_cache_key, offers, 30 * 60)
    context = {
        'user': user,
        'user_orders': user_orders,
        'user_order_item': user_order_item,
        'offers': offers
    }
    return render(request, 'app_users/account.html', context)



class AnotherLoginView(LoginView):
    template_name = 'app_users/login.html'
    next_page = '/'
    #logger.info(f'Пользователь {user} вошел в систему')



class AnotherLogoutView(LogoutView):
    next_page = '/'


def another_register_view(request):
    """регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user
                                   )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if request.user.is_authenticated:
                login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', {'form': form})

@login_required
def up_balance(request):
    if request.method == 'POST':
        user = Profile.objects.get(user=request.user)
        form = UpBalanceForm(request.POST)
        if form.is_valid():
            user.balance += int(request.POST.get('balance'))
            user.save()
            logger.info(f'Пользователь {user} пополнил баланс')
            return HttpResponseRedirect(reverse('account'))
    else:
        form = UpBalanceForm()
    return render(request, 'app_users/balance.html', {'form': form})


