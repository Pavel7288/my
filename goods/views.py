from django.shortcuts import render
from goods.models import Products


def catalog(request):
    products = Products.objects.all()

    context = {
        'title': 'Goods',
        'products': products
    }
    return render(request, 'main/catalog.html', context)


def product(request, product_slug):
    products = Products.objects.get(slug=product_slug)
    context = {
        'title': 'Description',
        'product': products
    }
    return render(request, 'main/description.html', context)


def make_order(request):
    context = {
        'title': 'Orders',
    }
    return render(request, 'main/basket.html', context)
