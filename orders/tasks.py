import time

from celery import shared_task
from django.core.exceptions import ValidationError
from django.db import transaction

from goods.models import Products
from orders.models import Order


@shared_task(bind=True,
             max_retries=3,
             default_retry_delay=10,      # задержка повторения
             acks_late=True,              # подтверждать задачу только после успешного выполнения
             reject_on_worker_lost=True   # возвращать задачу при сбое
             )
def add_to_queue(self,order_id, prod):
    print("🎯 Задача Celery запущена")
    time.sleep(10)
    try:
        with transaction.atomic():
            products_to_update = []
            order = Order.objects.get(id=order_id)
            order.status = 'Ваш заказ одобрен человечишка'
            order.save()
            for product_id_and_q in prod:
                product_id, product_quantity = product_id_and_q
                product = Products.objects.get(id=product_id)
                if product_quantity > product.quantity:
                    raise ValidationError(f"Недостаточное количество товара {product.name} на складе.")
                product.quantity -= product_quantity  # отнимаем количество из общего количества
                products_to_update.append(product)  # помещаем в список по одному продукты
            Products.objects.bulk_update(products_to_update, ['quantity'])  # сохраняем в бд сразу всё чтобы не ходить по 100 раз
            return 'Success'

    except ValidationError as ex:
        try:
            self.retry(exc=ex)
            raise 'Ошибка выполнения'
        except ValidationError as e:
            order.status = 'Ошибка при оформлении'
            order.save()
            raise e
