from django.contrib import admin
from .models import SiteSettings, HomePageContent, ContactMessage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    fieldsets = (
        ('Основное', {
            'fields': ('site_name', 'logo', 'favicon')
        }),
        ('Социальные сети', {
            'fields': ('instagram_url', 'telegram_url', 'whatsapp_url')
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'address', 'working_hours')
        }),
    )

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fieldsets = (
        ('Герой-секция', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_button_text')
        }),
        ('Блок "О нас"', {
            'fields': ('about_title', 'about_text', 'about_image')
        }),
        ('Блок "Доставка"', {
            'fields': ('delivery_title', 'delivery_text', 'delivery_image')
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')