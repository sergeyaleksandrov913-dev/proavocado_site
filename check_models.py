import os
import django

# Указываем Django, где находится settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proavocado.settings')

# Загружаем Django
django.setup()

# Теперь можно импортировать модели
from core.models import Category, Product

print("✅ Модели загружены успешно")
print("✅ Category:", Category)
print("✅ Product:", Product)