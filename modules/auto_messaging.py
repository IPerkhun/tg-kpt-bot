from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram import Bot
import asyncio

MESSAGES = {
    1: "Поздравляю! Уже через 1 час после отказа от сигарет твое сердце начинает биться ровнее, и давление приходит в норму. Ты уже на правильном пути!",
    3: "Прошло 3 часа без курения! Твой организм начинает снижать уровень никотина в крови. Продолжай, ты отлично справляешься!",
    5: "С момента последней сигареты прошло 5 часов. Кровообращение улучшается, и твое тело начинает восстанавливаться. Ты делаешь важные шаги к здоровью!",
    12: "Прошло 12 часов! Уровень угарного газа в крови снизился до нормы, и твое тело получает больше кислорода. Дышать становится легче!"
}

# Функция для отправки сообщений
async def send_message(bot: Bot, user_id: int, text: str):
    await bot.send_message(user_id, text, parse_mode="Markdown")

# Планировщик сообщений
def schedule_messages(bot: Bot, user_id: int, start_time: datetime):
    scheduler = AsyncIOScheduler()
    # Планируем каждое сообщение
    for hours, message in MESSAGES.items():
        send_time = start_time + timedelta(seconds=hours)
        scheduler.add_job(send_message, 'date', run_date=send_time, args=[bot, user_id, message])
    
    scheduler.start()

