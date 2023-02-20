from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *
from .models import Makeup
from reservations.views import MakeupDetailView

app_name = 'makeups'

urlpatterns = [
    path('', makeup_list, name='makeup_list'),
    path('makeups/', makeup_register, name='makeup_register'), 
    path('makeups/detail/<int:pk>/', MakeupDetailView.as_view(), name='makeup_detail'),
    path('makeups/detail/<int:pk>/makeup/',virtual_makeup, name='virtual_makeup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)