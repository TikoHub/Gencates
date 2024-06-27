from django.core.management.base import BaseCommand
import requests

TELEGRAM_BOT_TOKEN = '7298581946:AAFRLW1W3YIk4lOOT6EHqWtkaR62yT7_iTA'
WEBHOOK_URL = 'https://1dd3-5-251-138-54.ngrok-free.app/telegram-webhook/'
GAME_URL = 'https://takumishiawase.github.io/genecats/'


def set_webhook():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook'
    payload = {'url': WEBHOOK_URL}
    response = requests.post(url, json=payload)
    print(response.json())


class Command(BaseCommand):
    help = 'Set the Telegram webhook'

    def handle(self, *args, **kwargs):
        set_webhook()
