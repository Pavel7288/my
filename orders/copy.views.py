from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from cart.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    if request.method == "POST":  # Если POST — значит он отправил форму. Если GET — значит просто зашёл на страницу
        form = CreateOrderForm(data=request.POST)  # создаём новую форму
        if form.is_valid():  #в основном не проходит потому что не все параметры получены, если надо узнать
            #в чём дело то вставь else:print(form.errors)
            try:  # чтобы если была ошибка всё не накрылось
                with transaction.atomic():  # Это блок транзакции. Если в нём случается ошибка — ничего не сохраняется в БД.
                    user = request.user  # Получаем текущего залогиненного пользователя. Django сам прикрепляет user к объекту request, если пользователь авторизован.
                    cart_items = Cart.objects.filter(user=user)  # ищем товары этого пользователя и получаем связные объекты

                    if cart_items.exists():  # Проверяем, не пуста ли корзина. Если в ней ничего нет — заказ не создаём.
                        order = Order.objects.create(  # создаём заказ именно 1 заказ и привязываем их к пользователю
                            user=user,
                            delivery_address=form.cleaned_data['delivery_address'], #берём из формы параметры для полей
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
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
                                quantity=quantity,  #и количество
                            )
                            product.quantity -= quantity  # отнимаем количество из общего количества
                            product.save()  # сохраняем в бд

                        cart_items.delete()  # удаляем то что было в корзине

                        messages.success(request,'Заказ оформлен он появится в поле Мои заказы в ближайшее время')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e.messages[0]))
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