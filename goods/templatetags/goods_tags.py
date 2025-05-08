from django.utils.http import urlencode

from goods.models import Categories
from django import template

register = template.Library()


@register.simple_tag
def tag_categories():
    return Categories.objects.all()


@register.simple_tag(takes_context=True) #takes_context передаёт в функцию всё что есть в запросе
def change_param(context, **kwargs):   #context это всё что находится в url после ? и обновляет переданными параметрами например page=5 а было равно 2
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query) #urlncode это функция преобразует словарь в строку запроса url
# в общем эта функция копирует все текущие параметры из запроса и обновляет их переданными значениями а затем формирует строку запроса
#например у нас есть строка href="?{% change_param page=products.previous_page_number %} она берёт текущие параметры например страницу
# категорию и тд и обновляет то что ей передали а именно page, она как видишь, принимает бесконечно словарей


