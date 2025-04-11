# Generated by Django 4.2.19 on 2025-04-04 08:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен начинаться с + и содержать только цифры.', regex='^\\+\\d{1,14}$')], verbose_name=' номером телефона'),
        ),
    ]
