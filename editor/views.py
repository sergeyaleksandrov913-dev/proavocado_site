from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    """Страница контактов с формой"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо! Ваше сообщение отправлено.')
            return redirect('editor:contact')
    else:
        form = ContactForm()
    
    # Получаем настройки сайта для отображения контактной информации
    from .models import SiteSettings
    site_settings = SiteSettings.get_settings()
    
    context = {
        'form': form,
        'site_settings': site_settings,
    }
    return render(request, 'editor/contact.html', context)