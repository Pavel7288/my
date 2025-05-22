from celery import shared_task
import time

from django.contrib import messages

from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect, render

from cart.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from users.models import User


@shared_task
def add_to_queue(user_id, delivery_address, phone_number, requires_delivery, payment_on_get):
    print("🎯 Задача Celery запущена")
    time.sleep(10)
    try:
        with transaction.atomic():
            user = User.objects.get(id=user_id)
            cart_items = Cart.objects.filter(user=user)
            if cart_items.exists():  # Проверяем, не пуста ли корзина. Если в ней ничего нет — заказ не создаём.
                order = Order.objects.create(  # создаём заказ именно 1 заказ и привязываем их к пользователю
                    user=user,
                    delivery_address=delivery_address,
                    phone_number=phone_number,
                    requires_delivery=requires_delivery,
                    payment_on_get=payment_on_get,
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
                        status='Всё збс',
                    )
                    product.quantity -= quantity  # отнимаем количество из общего количества
                    product.save()  # сохраняем в бд

                cart_items.delete()  # удаляем то что было в корзине
                return 'Success'
            return 'None'
    except ValidationError:
        OrderItem.objects.create(
            order=order,
            product=product,
            name=name,
            price=price,
            quantity=quantity,
            status='Ошибка при оформлении повторите заказ',
        )
        product.save()
        return None