from django.forms import ModelForm
from django import forms

from .models import Makeup
from  products.models import Product

class MakeupModelForm(ModelForm):
    class Meta:
        model = Makeup
        fields = ['title', 'detail', 'image', 'products', 'price', 'status']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'products': forms.CheckboxSelectMultiple,
            'price' : forms.TextInput(attrs={'class': 'form-control'}), 
        }
        
        labels = {
            'products': '사용된 메이크업 제품',
            'image': '메이크업 이미지',
            'title': '제목',
            'detail': '설명',
            'price' : '예약료 (원/시간)'
        }  
