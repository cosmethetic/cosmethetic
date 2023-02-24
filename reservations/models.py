from django.db import models
from django.contrib.auth.models import User
from makeups.models import Makeup
from django.conf import settings

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='예약자')
    makeup = models.ForeignKey(Makeup, on_delete=models.CASCADE, verbose_name='메이크업 레퍼런스 이미지')
    start_time = models.DateTimeField(verbose_name='예약 시작 시간')
    end_time = models.DateTimeField(verbose_name='예약 종료 시간')
    total_fee = models.IntegerField(verbose_name='예약료')

    RENTAL_STATUS = (
        ('d', 'Default'),
        ('r', 'Request'),
        ('a', 'Accept'),
        ('c', 'Completed'),
    )

    status = models.CharField(
        max_length = 1,
        choices = RENTAL_STATUS,
        blank = True,
        default = 'd',
        help_text = 'reservation availability',
    )

    def __str__(self):
        return f'{self.user}님께서 {self.start_time}부터 {self.end_time}까지 예약한 <{self.makeup.title}>'
