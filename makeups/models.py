from config.models import Timestamp
from products.models import Product

import reserve as reserve
from django.db import models
from django.contrib.auth.models import User

class Makeup(Timestamp):
    products = models.ManyToManyField(Product, blank=True, verbose_name='사용 제품들')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    image = models.ImageField(upload_to='reference', verbose_name='메이크업 이미지')
    title = models.CharField(max_length=100, verbose_name='메이크업 제목')
    detail = models.TextField(verbose_name='메이크업 설명')
    price = models.IntegerField(verbose_name='메이크업 가격 (원/시간)')

    MAKEUP_STATUS = (
        ('a', 'available'),
        ('u', 'unavailable'),
    )

    status = models.CharField(
        max_length = 1,
        choices = MAKEUP_STATUS,
        blank = True,
        default = 'a',
        help_text = 'Makeup availability',
    )

    def get_absolute_url(self):
        return reserve('makeups:makeup_detail', args=[str(self.id)])
