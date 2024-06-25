from django.urls import path
from .views import login_view, telegram_webhook

urlpatterns = [
    path('login/', login_view, name='login'),
    path('telegram-webhook/', telegram_webhook, name='telegram_webhook'),

]
