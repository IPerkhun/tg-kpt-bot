from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta, time
from aiogram import Bot
from utils.content import MESSAGES
from utils.scheduler import get_scheduler

scheduler = get_scheduler()


async def send_message(bot: Bot, user_id: int, text: str):
    await bot.send_message(user_id, text, parse_mode="Markdown")


def schedule_messages(
    bot: Bot, user_id: int, start_time: datetime, start_hour=9, end_hour=18
):
    job_ids = []
    current_time = start_time

    for hours, message in MESSAGES.items():
        send_time = current_time + timedelta(hours=hours)

        # Проверяем, попадает ли время отправки в интервал 9:00 - 18:00
        if time(start_hour, 0) <= send_time.time() <= time(end_hour, 0):
            job = scheduler.add_job(
                send_message, "date", run_date=send_time, args=[bot, user_id, message]
            )
            job_ids.append(job.id)

    return job_ids
