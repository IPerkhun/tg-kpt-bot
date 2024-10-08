from modules.auto_messaging import schedule_messages, cancel_scheduled_messages
from db.data_manager import get_stop_smoking_data, update_stop_smoking_data
from datetime import datetime
from aiogram import types, Bot
import logging


logging.basicConfig(level=logging.INFO)


async def cmd_stop_smoking(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    stop_smoking_data = get_stop_smoking_data(user_id)

    if stop_smoking_data:
        cancel_scheduled_messages(stop_smoking_data["jobs"])
        logging.info(f"Cancelled scheduled messages for user {user_id}")

    stop_time = datetime.now()
    job_ids = schedule_messages(bot, user_id, stop_time)

    stop_smoking_data = {
        "time": stop_time.strftime("%Y-%m-%d %H:%M:%S"),
        "jobs": job_ids,
    }

    update_stop_smoking_data(user_id, stop_smoking_data)

    await message.answer(
        "Ты решил бросить курить! Я буду поддерживать тебя на этом пути и присылать сообщения с прогрессом."
    )
