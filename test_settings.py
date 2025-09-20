import os
import sys

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Указываем Django, где настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proavocado.settings')

import django
django.setup()

from django.conf import settings
print("✅ Django settings загружены")
print("📁 BASE_DIR:", settings.BASE_DIR)
print("🧩 INSTALLED_APPS:", 'core' in settings.INSTALLED_APPS)