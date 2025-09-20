# editor/views.py
from django.shortcuts import render

def index(request):
    """Главная страница редактора"""
    return render(request, 'editor/index.html')

def contact(request):
    """Страница контактов редактора"""
    return render(request, 'editor/contact.html')