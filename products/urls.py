from django.contrib import admin
from django.urls import path, include
from .views import product_list, product_detail

app_name = 'products'

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'), 
]

