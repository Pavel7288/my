from django.db import models

from goods.models import Products
from users.models import User


class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.product_cost() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины'

    objects = CartQuerySet().as_manager()

    def product_cost(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"Пользователь - {self.user} | Товар - {self.product.name} | Количество - {self.quantity}"  # мы можем использовать на методы классов на которые ссылаемся в ForeignKey
