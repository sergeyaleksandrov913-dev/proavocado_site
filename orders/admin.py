# orders/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """Вложенный список элементов заказа"""
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'get_cost')
    can_delete = False

    def get_cost(self, obj):
        """Рассчитать стоимость позиции"""
        if obj.pk:  # Только для существующих объектов
            return obj.get_cost()
        return 0
    get_cost.short_description = 'Стоимость'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка для заказов"""
    list_display = ('order_number', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'payment_id')
    readonly_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone', 
                      'delivery_address', 'total_amount', 'payment_id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    # Добавим действие для изменения статуса
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status='paid')
        self.message_user(request, f'{updated} заказ(ов) отмечены как оплаченные.')
    mark_as_paid.short_description = "Отметить как оплаченные"
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} заказ(ов) отмечены как отправленные.')
    mark_as_shipped.short_description = "Отметить как отправленные"
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} заказ(ов) отмечены как доставленные.')
    mark_as_delivered.short_description = "Отметить как доставленные"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} заказ(ов) отмечены как отмененные.')
    mark_as_cancelled.short_description = "Отметить как отмененные"

    # Кастомизация отображения статуса
    def status(self, obj):
        """Кастомное отображение статуса с цветами"""
        status_colors = {
            'new': 'orange',
            'paid': 'green',
            'shipped': 'blue',
            'delivered': 'purple',
            'cancelled': 'red',
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status.short_description = 'Статус'