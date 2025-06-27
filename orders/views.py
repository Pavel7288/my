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

            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)
                    products_all = []
                    order = Order.objects.create(  # создаём заказ именно 1 заказ и привязываем их к пользователю
                        user=user,
                        delivery_address=form.cleaned_data['delivery_address'],
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                        status='Товар оформляется и что-то может пойти не так',
                    )

                    for cart_item in cart_items:  # проходимся циклом по корзине текущего пользователя
                        product = cart_item.product  # это объект, мы ссылаемся по foreign key
                        name = cart_item.product.name  # берём название продукта
                        price = cart_item.product.price  # берём цену продукта
                        quantity = cart_item.quantity  # так же количество

                        if product.quantity < quantity:  # проверяем не больше ли заказали чем у нас на сладе
                            raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                             В наличии  {product.quantity}')  # если на складе меньше чем заказали поднимаем сообщение

                        OrderItem.objects.create(  # это создание записи в бд, одного товара
                            order=order,  # это ссылка на order
                            product=product,  # конкретный продукт
                            name=name,  # это название продукта
                            price=price,  # его название
                            quantity=quantity,  # и количество

                        )
                        products_all.append((product.id,quantity))
                        product.save()

                    cart_items.delete()
                    add_to_queue.delay_on_commit(
                        order_id=order.id,
                        prod=products_all
                    )
            except ValidationError as e:
                messages.success(request, str(e.messages[0]))
                return redirect('user:profile')


            messages.success(request, 'Заказ будет ждать оформления')
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


