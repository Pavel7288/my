from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import Products
from goods.utils import search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    query = request.GET.get('q')
    search_by_category = request.GET.get('category')
    if query:
        products = search(query,search_by_category).order_by('id')
    elif category_slug == 'all':
        products = Products.objects.all().order_by('id') # это можно сказать sql запрос SELECT * FROM Products и он помещает в переменную всё, что ты выбрал
    elif search_by_category:
        products = Products.objects.filter(category__slug=search_by_category).order_by('id')
    else:
        products = Products.objects.filter(category__slug=category_slug).order_by('id')   # category__slug это делается
# когда есть связь между таблицами, category это название столбца в Products, а slug - это поле модели Categories,
# которое мы хотим использовать для фильтрации. Эта вся строка буквально означает мы выведем все продукты у которых
#в категории находится та категория, которую мы прокинули, а __ - это синтаксис Django ORM для обращения к связным таблицам
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
