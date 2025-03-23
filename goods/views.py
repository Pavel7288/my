from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products


def catalog(request, category_slug):
    page = request.GET.get('page', 1)
    c = request.GET.get('category','all')
    if category_slug == 'all':
        products = Products.objects.all()
    else:
        products = get_list_or_404(Products.objects.filter(category__slug=category_slug))
    paginator = Paginator(products, 1)
    current_page = paginator.page(page)
    context = {
        'title': 'Goods',
        'products': current_page,
        'category_slug': c,
        'page': page,
        'slug': category_slug,

    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    products = Products.objects.get(slug=product_slug)
    context = {
        'title': 'Description',
        'product': products,
    }
    return render(request, 'goods/product.html', context)


def make_order(request):
    context = {
        'title': 'Orders',
    }
    return render(request, 'goods/basket.html', context)
