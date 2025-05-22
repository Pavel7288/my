from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import Products
from goods.utils import search


def get_products_from_cache(s_by_category=None,c_slug=None):
    if not s_by_category:
        cache_key = f'products_{c_slug}'
    else:
        cache_key = f'products_{s_by_category}'
    cached_products = cache.get(cache_key)   # получаем из кэша нужные данные по ключу
    if cached_products is None:  # если данных нет, то вручную берём нужный объект
        if c_slug == 'all':
            products = Products.objects.all().order_by('id') # это можно сказать sql запрос SELECT * FROM Products и он помещает в переменную всё, что ты выбрал
        elif s_by_category:
            products = Products.objects.filter(category__slug=s_by_category).order_by('id')
        else:
            products = Products.objects.filter(category__slug=c_slug).order_by('id')   # category__slug это делается
        cache.set(key=cache_key, value=products, timeout=60)  # и кешируем его по ключу, данным и времени жизни кэша
    # когда есть связь между таблицами, category это название столбца в Products, а slug - это поле модели Categories,
    # которое мы хотим использовать для фильтрации. Эта вся строка буквально означает мы выведем все продукты у которых
    #в категории находится та категория, которую мы прокинули, а __ - это синтаксис Django ORM для обращения к связным таблицам
    else:
        products = cached_products   # возвращаем products в любом случае поэтому переопределяем cached_products

    return products

def catalog(request, category_slug=None):
    search_by_category = request.GET.get('category')
    query = request.GET.get('q')
    page = request.GET.get('page', 1)
    if query:
        products = search(query, search_by_category).order_by('id')
    else:
        products = get_products_from_cache(s_by_category=search_by_category,c_slug=category_slug)
    paginator = Paginator(products, 4)
    current_page = paginator.page(int(page))
    context = {
        'request_slug': search_by_category,
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
