from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True, verbose_name='URL')
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(default=1, verbose_name='Цена')
    image = models.ImageField(upload_to='goods_images', verbose_name='Изображение')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        db_table = 'product'
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    def display_id(self):
        return f'{self.id:05}'
