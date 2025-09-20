from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from orders.models import Order

# Проверка, что пользователь является администратором
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    """Панель управления заказами"""
    # Получаем статистику
    total_orders = Order.objects.count()
    new_orders = Order.objects.filter(status='new').count()
    paid_orders = Order.objects.filter(status='paid').count()
    
    # Получаем последние заказы
    recent_orders = Order.objects.all()[:10]
    
    context = {
        'total_orders': total_orders,
        'new_orders': new_orders,
        'paid_orders': paid_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'orders_admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def order_list(request):
    """Список всех заказов"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Фильтрация по статусу (если передан параметр)
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'current_status': status,
    }
    return render(request, 'orders_admin/order_list.html', context)

@login_required
@user_passes_test(is_admin)
def order_detail(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'orders_admin/order_detail.html', context)

@login_required
@user_passes_test(is_admin)
def change_order_status(request, order_id):
    """Изменение статуса заказа"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Статус заказа #{order.order_number} изменен на {order.get_status_display()}')
        else:
            messages.error(request, 'Неверный статус')
    
    return redirect('orders_admin:order_detail', order_id=order_id)