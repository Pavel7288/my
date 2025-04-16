from django.contrib import admin

from cart.admin import CartTabAdmin
from orders.admin import OrderTabularAdmin
from users.models import User


# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'email']

    inlines = [CartTabAdmin,OrderTabularAdmin]