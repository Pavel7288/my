from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=150,unique=True,null=True,blank=True)