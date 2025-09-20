from django.db import models
from core.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    order_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заказа")
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_email = models.EmailField(verbose_name="Email клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма заказа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    payment_id = models.CharField(max_length=100, blank=True, verbose_name="ID платежа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу") # Цена на момент заказа

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
    def get_cost(self):
        """Рассчитать стоимость позиции"""
        return self.price * self.quantity