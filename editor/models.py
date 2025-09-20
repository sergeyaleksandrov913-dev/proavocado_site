# editor/models.py
from django.db import models

class SiteSettings(models.Model):
    """Настройки сайта"""
    site_name = models.CharField(max_length=200, default="Pro🥑ПИТАНИЕ", verbose_name="Название сайта")
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Логотип")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Фавикон")
    
    # Социальные сети
    instagram_url = models.URLField(blank=True, verbose_name="Ссылка на Instagram")
    telegram_url = models.URLField(blank=True, verbose_name="Ссылка на Telegram")
    whatsapp_url = models.URLField(blank=True, verbose_name="Ссылка на WhatsApp")
    
    # Контакты
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Адрес")
    working_hours = models.CharField(max_length=100, blank=True, verbose_name="Режим работы")
    
    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    @classmethod
    def get_settings(cls):
        """Получить или создать настройки сайта"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class HomePageContent(models.Model):
    """Контент главной страницы"""
    # Герой-секция
    hero_title = models.CharField(max_length=200, default="Pro<span style='color: #87B741;'>&#129734;</span>ПИТАНИЕ", verbose_name="Заголовок героя")
    hero_subtitle = models.TextField(default="Гастрономическое кафе с полезными и вкусными блюдами из натуральных продуктов", verbose_name="Подзаголовок героя")
    hero_button_text = models.CharField(max_length=50, default="Смотреть меню", verbose_name="Текст кнопки героя")
    
    # Блок "О нас"
    about_title = models.CharField(max_length=200, default="О нашем кафе", verbose_name="Заголовок блока 'О нас'")
    about_text = models.TextField(default="Pro&#129734;ПИТАНИЕ — это место, где вкус и польза идут рука об руку...", verbose_name="Текст блока 'О нас'")
    about_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Изображение блока 'О нас'")
    
    # Блок "Доставка"
    delivery_title = models.CharField(max_length=200, default="Доставка", verbose_name="Заголовок блока 'Доставка'")
    delivery_text = models.TextField(default="Мы предлагаем удобную доставку готовых блюд...", verbose_name="Текст блока 'Доставка'")
    delivery_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Изображение блока 'Доставка'")
    
    class Meta:
        verbose_name = "Контент главной страницы"
        verbose_name_plural = "Контент главной страницы"

    def __str__(self):
        return "Контент главной страницы"

    @classmethod
    def get_content(cls):
        """Получить или создать контент главной страницы"""
        content, created = cls.objects.get_or_create(pk=1)
        return content


class ContactMessage(models.Model):
    """Сообщения из формы контактов"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Сообщение из формы контактов"
        verbose_name_plural = "Сообщения из формы контактов"
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение от {self.name}: {self.subject}"