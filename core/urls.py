from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('checkout/', views.create_order, name='create_order'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('webhook/yookassa/', views.yookassa_webhook, name='yookassa_webhook'),
]