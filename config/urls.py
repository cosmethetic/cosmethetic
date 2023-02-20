from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('makeups.urls')), 
    path('', include('products.urls')), 
    path('', include('carts.urls')), 
    path('', include('reservations.urls')), 
    path('accounts/', include('allauth.urls')),
]
