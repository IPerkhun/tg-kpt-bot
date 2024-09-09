from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram import Bot
from utils.content import MESSAGES

scheduler = AsyncIOScheduler()

if not scheduler.running:
    scheduler.start()

async def send_message(bot: Bot, user_id: int, text: str):
    await bot.send_message(user_id, text, parse_mode="Markdown")

def schedule_messages(bot: Bot, user_id: int, start_time: datetime):
    job_ids = []

    for hours, message in MESSAGES.items():
        send_time = start_time + timedelta(hours=hours)
        job = scheduler.add_job(send_message, 'date', run_date=send_time, args=[bot, user_id, message])
        job_ids.append(job.id)
    
    return job_ids

def cancel_scheduled_messages(job_ids):
    for job_id in job_ids:
        try:
            scheduler.remove_job(job_id)
        except Exception as e:
            print(f"Ошибка при отмене задачи {job_id}: {e}")
