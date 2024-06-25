# game/management/commands/runbot.py

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from django.conf import settings
from django.core.management.base import BaseCommand
from game.models import TelegramUser, UserProfile
from django.contrib.auth.models import User


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создание пользователя Telegram
    telegram_user, created = await TelegramUser.objects.aget_or_create(user_id=update.effective_user.id, defaults={
        'username': update.effective_user.username,
        'first_name': update.effective_user.first_name,
        'last_name': update.effective_user.last_name,
    })

    if created:
        await update.message.reply_text(f'Welcome, {update.effective_user.first_name}!')
    else:
        await update.message.reply_text(f'Welcome back, {update.effective_user.first_name}!')

    # Создание пользователя Django, если он не существует
    django_user, created = await User.objects.aget_or_create(username=update.effective_user.username, defaults={
        'first_name': update.effective_user.first_name,
        'last_name': update.effective_user.last_name,
        'email': f'{update.effective_user.username}@example.com',  # Пример email
    })

    if created:
        UserProfile.objects.create(user=django_user)  # Создание профиля пользователя

    # Отправка реферальной ссылки
    referral_link = f"http://127.0.0.1:3000/register?ref={django_user.userprofile.referral_code}"
    await update.message.reply_text(f'Your referral link: {referral_link}')

    # Отправка ссылки на демо-версию игры
    demo_link = f"http://127.0.0.1:3000/demo?user={django_user.username}"
    await update.message.reply_text(f'Play the demo here: {demo_link}')


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        django_user = await User.objects.aget(username=update.effective_user.username)
        profile = await UserProfile.objects.aget(user=django_user)
        response = f"User: {django_user.username}\nCoins: {profile.coins}\nLevel: {profile.level}"
        await update.message.reply_text(response)
    except User.DoesNotExist:
        await update.message.reply_text('You are not registered in our system.')


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) != 1:
        await update.message.reply_text('Usage: /register <referral_code>')
        return

    referral_code = args[0]
    try:
        django_user = await User.objects.aget(username=update.effective_user.username)
        referrer = await UserProfile.objects.aget(referral_code=referral_code)
        profile = await UserProfile.objects.aget(user=django_user)
        profile.referred_by = referrer
        profile.save()

        # Пример начисления бонусов
        referrer.coins += 100
        referrer.save()
        profile.coins += 50
        profile.save()

        await update.message.reply_text(
            f'Successfully registered with referral code. You received 50 coins. Your referrer received 100 coins.')
    except User.DoesNotExist:
        await update.message.reply_text('You are not registered in our system.')
    except UserProfile.DoesNotExist:
        await update.message.reply_text('Invalid referral code.')


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        django_user = await User.objects.aget(username=update.effective_user.username)
        await update.message.reply_text('Starting the demo...')

        # Ссылка на демо-версию игры
        demo_link = f"http://127.0.0.1:3000/demo?user={django_user.username}"
        await update.message.reply_text(f'Play the demo here: {demo_link}')
    except User.DoesNotExist:
        await update.message.reply_text('You are not registered in our system.')


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("profile", profile))
        application.add_handler(CommandHandler("register", register))
        application.add_handler(CommandHandler("play", play))

        application.run_polling()
