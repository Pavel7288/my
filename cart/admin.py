from django.contrib import admin

from cart.models import Cart

# так мы регистрируем новые таблицы которые мы создали

class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ("product", 'quantity','date')
    readonly_fields = ("date",)
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ["user", "product__name", ]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    def product_display(self, obj):
        return str(obj.product.name)

    # user_display and product_display alter name of columns in admin panel
    user_display.short_description = "Пользователь"
    product_display.short_description = "Товар"