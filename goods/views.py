from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products
from goods.utils import search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)
    search_by_category = request.GET.get('category', None)
    if query:
        products = search(query,search_by_category)
    elif category_slug == 'all':
        products = Products.objects.all() # это можно сказать sql запрос SELECT * FROM Products и он помещает в переменную всё что ты выбрал
    else:
        products = get_list_or_404(Products, category__slug=category_slug) # category__slug это делается когда есть связь между таблицами, category это
        # название столбца в Products, а slug - это поле модели Categories, которое мы хотим использовать для фильтрации. Эта вся строка буквально
        # означает мы выведем ошибку если не найдём ни одного объекта, а если найдём, то выведем все продукты у которых в категории находится та категория которую мы прокинули
        # а __ это синтаксис Django ORM для обращения к связным таблицам
    paginator = Paginator(products, 4)
    current_page = paginator.page(int(page))
    context = {
        'l': search_by_category,
        'title': 'Goods',
        'products': current_page,
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
