# orders_admin/urls.py
from django.urls import path
from . import views

app_name = 'orders_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/change-status/', views.change_order_status, name='change_order_status'),
]