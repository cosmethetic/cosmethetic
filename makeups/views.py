import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect

from accounts.models import Profile

from .models import Makeup
from .forms import MakeupModelForm 

def makeup_list(request):
    makeups = Makeup.objects.all()
    return render(request, 'makeups/index.html', {'makeups': makeups})

@login_required(login_url="/login")
def makeup_register(request):
    if request.method == 'POST':
        form = MakeupModelForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            makeup = Makeup.objects.create(
                image=data['image'],
                title=data['title'],
                detail=data['detail'],
            )

            products = data.get('products')
            for product in products.iterator():
                makeup.products.add(product)

            makeup.save()

            return redirect('makeups:makeup_detail', pk=makeup.id)
    else:
        form = MakeupModelForm()
    return render(request, 'makeups/makeup_register.html', {'form': form})


def makeup_detail(request, pk):
    makeup = Makeup.objects.get(pk=pk)
    products = makeup.products.all()
    return render(request, 'makeups/makeup_detail.html', {'object': makeup, 'products': products})

@login_required(login_url="/login")
def virtual_makeup(request, pk):
    makeup = Makeup.objects.get(pk=pk)

    makeup_image = str(makeup.image)
    user_image = str(request.user.profile.image)

    root = 'CPM/imgs/'

    save_path = root + 'results/'

    cmd = f'CUDA_VISIBLE_DEVICES=0 python CPM/main.py --style {root}{makeup_image} --input {root}{user_image}  --savedir {save_path} --filename {pk}_{request.user.id}.png'

    os.system(cmd)

    result = f'/{save_path}{pk}_{request.user.id}.png'

    return render(request, 'makeups/result.html', {'makeup': makeup, 'result': result})




