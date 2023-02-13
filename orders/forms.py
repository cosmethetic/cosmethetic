from django import forms
from django.contrib.auth.models import User

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['emailAddress', 'shippingPostcode']
