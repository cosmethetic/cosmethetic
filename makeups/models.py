from config.models import Timestamp
from products.models import Product

import reserve as reserve
from django.db import models
from django.contrib.auth.models import User

class Makeup(Timestamp):
    products = models.ManyToManyField(Product, blank=True)
    image = models.ImageField(upload_to='reference')
    title = models.CharField(max_length=100)
    detail = models.TextField()

    def get_absolute_url(self):
        return reserve('makeups:makeup_detail', args=[str(self.id)])
