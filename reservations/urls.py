from django.contrib import admin
from django.urls import path, include
from .views import ReservationDetailView

app_name = 'reservations'

urlpatterns = [
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation_detail'),
]
