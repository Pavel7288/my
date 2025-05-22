from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from cart.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from orders.tasks import add_to_queue


@login_required
def create_order(request):
    if request.method == "POST":  # Если POST — значит он отправил форму. Если GET — значит просто зашёл на страницу
        form = CreateOrderForm(data=request.POST)  # создаём новую форму
        if form.is_valid():  # в основном не проходит потому что не все параметры получены, если надо узнать
            user = request.user
            cart_items = Cart.objects.filter(user=user)
            for cart_item in cart_items:
                if cart_item.product.quantity < cart_item.quantity:
                    messages.warning(request, f'Недостаточное количество товара {cart_item.product.name} на складе\
                         В наличии  {cart_item.product.quantity}')
                    return redirect('user:profile')

            add_to_queue.delay(
                user_id=user.id,
                delivery_address=form.cleaned_data['delivery_address'],
                phone_number=form.cleaned_data['phone_number'],
                requires_delivery=form.cleaned_data['requires_delivery'],
                payment_on_get=form.cleaned_data['payment_on_get'],
            )
            messages.success(request, 'Заказ оформлен он появится в поле Мои заказы в ближайшее время')
            return redirect('user:profile')
    else:
        initial = {
            'username': request.user.username,  # если вызываем метод get, то подставляем в поля значения
            'phone_number': request.user.number,
        }
        form = CreateOrderForm(initial=initial)  # если get запрос создаём форму передавая initial
    context = {
        'title': "Оформление заказа",
        'form': form,
    }
    return render(request, 'orders/order.html', context)