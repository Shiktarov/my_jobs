import logging
from time import asctime
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User
from app_users.models import Profile
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

logger = logging.getLogger(__name__)

@transaction.atomic
def update_balance(scores, request):
    author = Profile.objects.get(user=request.user)
    author.plus_point(scores)
    author.minus_balance(scores)
    author.isstatus()

def order_create(request):
    cart = Cart(request)
    user = User.objects.get(username=request.user)
    profile = user.profile
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            logger.info(f'{user} сделал заказ')
            summ = 0
            summ += cart.get_total_price()
            profile.balance -= summ
            logger.info(f'{user} списано с баланса {summ}')
            profile.points += summ
            profile.isstatus()
            logger.info(f'статус {user} изменен')
            profile.save()
            for item in cart:
                OrderItem.objects.create(
                                        order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'app_orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm(instance=profile)
    return render(request, 'app_orders/create.html',
                  {'cart': cart, 'form': form})