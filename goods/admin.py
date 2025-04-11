from django.contrib import admin

from goods.models import Categories, Products


# admin.site.register(Categories)
# admin.site.register(Products)
# так мы регистрируем новые таблицы которые мы создали
# это надо будет ещё понять хз что тут происходит

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name','price','quantity']
    list_editable = ['price','quantity']
    search_fields = ['name', 'description']
    fields = [
        ('name','slug'),
        'category',
        'description',
        'price',
        'quantity',
        'image',
    ]
