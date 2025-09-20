from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'get_cost')

    def get_cost(self, obj):
        if obj.pk:  # Только для существующих объектов
            return obj.get_cost()
        return 0
    get_cost.short_description = 'Стоимость'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email')
    readonly_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone', 
                      'delivery_address', 'total_amount', 'payment_id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    # Добавим действие для изменения статуса
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_as_paid.short_description = "Отметить как оплаченные"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = "Отметить как отправленные"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "Отметить как доставленные"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Отметить как отмененные"