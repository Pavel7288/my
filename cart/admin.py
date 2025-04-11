from django.contrib import admin

from cart.models import Cart

# так мы регистрируем новые таблицы которые мы создали

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
