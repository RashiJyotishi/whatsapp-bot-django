# botapp/urls.py

from django.urls import path
from .views import whatsapp_bot

urlpatterns = [
    path('bot', whatsapp_bot, name='whatsapp-bot'),
]
