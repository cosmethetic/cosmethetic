from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *
from .models import Cart

app_name = 'carts'

urlpatterns = [
    path('add/<int:product_id>/', add_cart, name='add_cart'),
    path('carts/', cart_detail, name='cart_detail'),
    path('carts/remove/<int:product_id>/', cart_remove, name='cart_remove'), 
    path('carts/remove-all//<int:product_id>', cart_all_remove, name='cart_all_remove'), 
]
