from django.urls import path

from goods import views

app_name = "goods"



urlpatterns = [
    path('search/', views.catalog, name='search'),
    # category_slug>/' это передаётся в функцию на которую ссылается этот путь иначе не поймёт
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]




