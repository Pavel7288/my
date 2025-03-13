from django.urls import path

import goods.views

app_name = "goods"
urlpatterns = [
    path('', goods.views.catalog, name='catalog'),
    path('product/', goods.views.make_order, name='product'),
]
