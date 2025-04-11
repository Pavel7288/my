from django.http import JsonResponse
from django.template.loader import render_to_string

from cart.models import Cart
from cart.utils import get_user_carts
from goods.models import Products


def cart_add(request):
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)  # создаём объект product и получаем по слагу сам продукт, а не просто переданную строку product_slug
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user,product=product)  # затем создаём карту где фильтруем по имени пользователя и товару
        # мы можем обращаться к user из-за того что у нас в таблице есть колонка user которая ссылается на него в таблице
        if carts.exists():
            cart = carts[0]  # берём первый товар в карте потому что только одно название товара может содержаться в одной карте клиента
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product,quantity=1)  # если карты нет, то сохраняем карту с одним объектом продукта
    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if carts.exists():
            cart = carts[0]
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product,quantity=1)
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        'cart/cart_items.html',{'carts':user_cart}, request=request)
    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html,
    }
    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get('cart_id', None)
    quantity = request.POST.get('quantity', None)
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        'cart/cart_items.html', {'carts': user_cart}, request=request)

    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html,
        'quantity': cart.quantity,
    }
    return JsonResponse(response_data)


def cart_remove(request):
    print("POST:", request.POST)
    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        'cart/cart_items.html', {'carts': user_cart}, request=request)
    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html,
    }
    return JsonResponse(response_data)
