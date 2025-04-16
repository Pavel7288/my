from django.db import models

from goods.models import Products
from users.models import User

#Это расширение стандартного QuerySet. То есть я создаю свой класс,
# который добавляет дополнительные методы к обычным запросам через ORM.
# и теперь я смогу вызвать вот так это OrderItem.objects.total_price()
#OrderItem.objects.total_quantity()
class OrderitemQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name='Пользователь',default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"

    def __str__(self):
        username = self.user.username if self.user else f"аноним"
        return f"Заказ № {self.pk} | Покупатель {username}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name='Продукт',default=None)
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.IntegerField(default=1, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    objects = OrderitemQuerySet.as_manager()

    def products_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'Товар {self.name} | Заказ № {self.order.pk}'
