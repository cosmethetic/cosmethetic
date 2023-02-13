from django.shortcuts import render
from .models import Product, Category
from django.views.generic import View

def product_list(request):
    product_list = Product.objects.all()
    category_list = Category.objects.all()
     
    context = {
        'product_list': product_list, 
        'category_list': category_list, 
    }

    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'products/product_detail.html', {'object': product})
