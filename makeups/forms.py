from django.forms import ModelForm
from django import forms

from .models import Makeup
from  products.models import Product

class MakeupModelForm(ModelForm):
    class Meta:
        model = Makeup
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'products': forms.CheckboxSelectMultiple,
        }
        
        labels = {
            'products': '사용된 메이크업 제품',
            'image': '메이크업 이미지',
            'title': '이름',
            'detail': '설명',
        }  
