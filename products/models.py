from config.models import Timestamp

import reserve as reserve

from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, default='no-category')

    def get_absolute_url(self):
        return f'/products/{self.slug}'



class Product(Timestamp):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category', null=True)
    image = ImageField(upload_to='product')
    detail_image = ImageField(upload_to='product_detail')
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    description = models.TextField()

    def get_absolute_url(self):
        return reserve('product:product_detail', args=[str(self.id)])

    def __str__(self):
        return '{}'.format(self.name)

        
