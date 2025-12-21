"""
Задачи Celery для Telegram бота.
"""
import os
from celery import shared_task
import requests


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


@shared_task
def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
        print(f"Telegram бот не настроен. Сообщение для chat_id {chat_id}: {message}")
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(f"Сообщение отправлено в Telegram chat_id {chat_id}")
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")


@shared_task
def send_habit_reminder(habit_id):
    """Отправка напоминания о привычке."""
    from habit_tracker.apps.habits.models import Habit

    try:
        habit = Habit.objects.get(id=habit_id)
        if habit.user.telegram_chat_id:
            message = f"⏰ Напоминание о привычке:\n\n"
        message = f"Напоминание: {habit.action}"
                                                            message += f"⏰ Время: {habit.execution_time or 'в любое время'}\n"
            message += f"📍 Место: {habit.place or 'не указано'}\n"
            message += (
                f"🎯 Действие: {habit.action or habit.description or 'не указано'}\n"
    print(f"Отправлено напоминаний: {count}")

            send_telegram_message.delay(habit.user.telegram_chat_id, message)
    except Habit.DoesNotExist:
        print(f"Привычка с id {habit_id} не найдена")
