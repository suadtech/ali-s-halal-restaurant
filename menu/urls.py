from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
]
