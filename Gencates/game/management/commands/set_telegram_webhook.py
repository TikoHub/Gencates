from django.core.management.base import BaseCommand
import logging
from aiogram import Bot, Dispatcher, types, Router, F
from aiohttp import web
from django.conf import settings
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_TOKEN
WEBHOOK_HOST = 'https://1dd3-5-251-138-54.ngrok-free.app'
WEBHOOK_PATH = '/telegram-webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 8000

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

GAME_URL = 'https://takumishiawase.github.io/genecats/'  # URL вашей игры

def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🎮 Play the Game!",
        web_app=WebAppInfo(
            url=GAME_URL
        )
    )
    return builder.as_markup()

@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    await message.reply(
        "Welcome to the bot! Click the button below to start the game.",
        reply_markup=webapp_builder()
    )

@router.message(F.text == "/play")
async def play_game(message: types.Message):
    await bot.send_game(chat_id=message.chat.id, game_short_name="Gencates")

@router.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    logging.warning('Bye!')

async def handle_update(request):
    update = await request.json()
    await dp.feed_update(bot, types.Update(**update))
    return web.Response()

class Command(BaseCommand):
    help = 'Run the Telegram bot with webhook'

    def handle(self, *args, **kwargs):
        app = web.Application()
        app.router.add_post(WEBHOOK_PATH, handle_update)
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)

        dp.include_router(router)

        web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
