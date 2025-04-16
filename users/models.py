from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    number_validator = RegexValidator(regex=r'^\+\d{6,14}$', message="Номер телефона должен начинаться с + и содержать только цифры, минимум 6.")
    image = models.ImageField(upload_to='goods_images', null=True, blank=True)
    number = models.CharField(unique=True, null=True, blank=True, max_length=15, validators=[number_validator],verbose_name=" номером телефона")