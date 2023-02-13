from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.forms import OrderForm 

from django.core.exceptions import ObjectDoesNotExist

def get_cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    
    return cart

@login_required(login_url="/login")
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = get_cart_id(request),
            user = request.user
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity < cart_item.product.quantity:
            cart_item.quantity +=1 
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product, 
            quantity = 1, 
            cart = cart, 
            active = True 
        )
        cart_item.save()

    return redirect('carts:cart_detail')

@login_required(login_url="/login")
def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
        
        order_form = OrderForm()

    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        user = request.user
        emailAddress = request.POST['emailAddress']
        shippingPostcode = request.POST['shippingPostcode']

        try:
            order_details = Order.objects.create(
                user = request.user, 
                total = total, 
                emailAddress = emailAddress,
                shippingPostcode = shippingPostcode 
            )
            order_details.save()

            for order_item in cart_items:
                oi = OrderItem.objects.create(
                    product = order_item.product.name,
                    quantity = order_item.quantity,
                    price = order_item.product.price,  
                    order = order_details
                )
                oi.save()

                products = Product.objects.get(id=order_item.product.id)
                products.quantity = int(order_item.product.quantity - order_item.quantity)
                products.save()
                order_item.delete()

                print('주문이 완료되었습니다.')

            return redirect('/')
        except ObjectDoesNotExist:
            pass 

    return render(request, 'carts/cart.html', dict(cart_items = cart_items, total = total, counter = counter, order_form = OrderForm))

@login_required(login_url="/login")
def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()
    
    return redirect('carts:cart_detail')

@login_required(login_url="/login")
def cart_all_remove(request, product_id):
    cart = Cart.objects.get(cart_id = get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('carts:cart_detail')

