# core/views.py
import uuid
import json
from yookassa import Payment
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product, Category
from orders.models import Order, OrderItem
from editor.models import SiteSettings, HomePageContent

def index(request):
    # Получаем настройки сайта
    site_settings = SiteSettings.get_settings()
    home_content = HomePageContent.get_content()
    
    # Получаем все активные товары и категории
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    context = {
        'site_settings': site_settings,  # Передаём настройки
        'home_content': home_content,    # Передаём контент главной
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)


def category_detail(request, category_slug):
    """Страница детальной информации о категории"""
    category = get_object_or_404(Category, slug=category_slug)
    products = category.products.filter(is_active=True)
    
    # Получаем все категории для бокового меню
    categories = Category.objects.all()
    
    # Получаем настройки сайта
    site_settings = SiteSettings.get_settings()
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'site_settings': site_settings,
    }
    return render(request, 'core/category_detail.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Получаем настройки сайта
    site_settings = SiteSettings.get_settings()
    context = {
        'product': product,
        'site_settings': site_settings,
    }
    return render(request, 'core/product_detail.html', {'product': product, 'site_settings': site_settings})


def create_order(request):
    """Страница оформления заказа"""
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            customer_name = request.POST.get('name')
            customer_email = request.POST.get('email')
            customer_phone = request.POST.get('phone')
            delivery_address = request.POST.get('address')
            
            # Получаем данные корзины из скрытого поля (в формате JSON)
            cart_data_json = request.POST.get('cart')
            if not cart_data_json:
                # Можно вернуть ошибку
                pass
            
            cart_data = json.loads(cart_data_json)
            
            if not cart_data:
                # Можно вернуть ошибку
                pass

            # Рассчитываем общую сумму
            total_amount = 0
            order_items_data = []
            for item_data in cart_data:
                product_id = item_data['id']
                quantity = int(item_data['qty'])
                # Получаем актуальную цену товара из базы
                try:
                    product = Product.objects.get(id=product_id, is_active=True)
                    item_total = product.price * quantity
                    total_amount += item_total
                    order_items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price': product.price
                    })
                except Product.DoesNotExist:
                    # Игнорируем несуществующие или неактивные товары
                    continue
            
            if total_amount <= 0:
                # Можно вернуть ошибку
                pass

            # Создаем заказ в базе данных
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            order = Order.objects.create(
                order_number=order_number,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                delivery_address=delivery_address,
                total_amount=total_amount,
            )
            
            # Создаем элементы заказа
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
            
            # Создаем платеж через ЮKassa
            payment = Payment.create({
                "amount": {
                    "value": f"{total_amount:.2f}",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.build_absolute_uri('/payment/success/')
                },
                "capture": True,
                "description": f"Заказ {order_number}",
                "metadata": {
                    "order_id": order.id,
                }
            })
            
            # Сохраняем ID платежа в заказе
            order.payment_id = payment.id
            order.save()
            
            # Перенаправляем пользователя на страницу оплаты
            return redirect(payment.confirmation.confirmation_url)
            
        except Exception as e:
            # В production лучше логировать ошибку
            print(f"Ошибка при создании заказа: {e}")
            # Можно показать сообщение об ошибке пользователю
            # Для простоты просто редиректим обратно на форму
            pass

    # Если GET запрос или ошибка, показываем форму
    # Нужно передать данные корзины в шаблон, чтобы показать их пользователю
    # Для простоты можно оставить пустую форму, а данные корзины будут переданы через JS
    # Получаем настройки сайта для футера
    site_settings = SiteSettings.get_settings()
    return render(request, 'core/checkout.html', {'site_settings': site_settings})
# Добавляем вебхук для ЮKassa
@csrf_exempt
@require_POST
def yookassa_webhook(request):
    """Обработчик вебхука от ЮKassa"""
    try:
        # Получаем данные из вебхука
        data = json.loads(request.body)
        print(f"Получен вебхук: {data}") # Для отладки
        
        # Обрабатываем событие
        if data.get('event') == 'payment.succeeded':
            # Получаем ID платежа и метаданные
            payment_id = data['object'].get('id')
            metadata = data['object'].get('metadata', {})
            order_id = metadata.get('order_id')
            
            if order_id:
                # Обновляем статус заказа
                try:
                    order = Order.objects.get(id=order_id)
                    if order.status != 'paid': # Избегаем двойного обновления
                        order.status = 'paid'
                        order.save()
                        print(f"Заказ {order.order_number} обновлен до 'paid'")
                        
                        # Здесь можно отправить уведомление администратору
                        # send_admin_notification(order)
                        # Или отправить email клиенту
                        # send_customer_confirmation(order)
                        
                except Order.DoesNotExist:
                    print(f"Заказ с id={order_id} не найден для платежа {payment_id}")
            else:
                print(f"Метаданные заказа отсутствуют в платеже {payment_id}")
        
        # Возвращаем успешный ответ
        return HttpResponse(status=200)
        
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON из вебхука")
        return HttpResponse(status=400) # Bad Request
    except Exception as e:
        # В production лучше логировать ошибку в файл или систему логирования
        print(f"Ошибка обработки вебхука: {e}")
        return HttpResponse(status=500) # Internal Server Error


def payment_success(request):
    """Страница успешной оплаты"""
    # Можно получить order_number из параметров запроса
    # Но так как мы перенаправляем с ЮKassa, там может не быть наших параметров
    # Лучше искать по payment_id, который ЮKassa может передать
    
    # Простой вариант - показываем общий успех
    # Получаем настройки сайта для футера
    site_settings = SiteSettings.get_settings()
    return render(request, 'core/payment_success.html', {'site_settings': site_settings})