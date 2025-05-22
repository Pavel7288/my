from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_redis.cache import RedisCache
from goods.models import Products


@receiver(post_save, sender=Products)
@receiver(post_delete, sender=Products)
def clear_products_cache(sender, instance, **kwargs):
    if isinstance(cache, RedisCache):  # без этого тоже будет работать, но ide не будет видеть delete_pattern
        pass
    cache.delete_pattern(f'products_{instance.category.slug}')
    cache.delete_pattern(f'products_all')
