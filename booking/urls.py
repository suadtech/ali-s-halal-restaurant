from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_form, name='booking_form'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
