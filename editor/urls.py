from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
]