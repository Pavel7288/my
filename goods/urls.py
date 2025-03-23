from django.urls import path

from goods import views

app_name = "goods"
urlpatterns = [
    path('залупа_коня/<slug:category_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]
