from modules.auto_messaging import schedule_messages, cancel_scheduled_messages
from db.stop_smoking import (
    get_stop_smoking_data,
    update_stop_smoking_data,
    delete_stop_smoking_data,
)
from datetime import datetime, timedelta
from aiogram import types, Bot
import logging
from utils.content import (
    STOP_SMOKING_INFO,
    STOP_SMOKING_ALREADY_STARTED,
    STOP_SMOKING_CANCELLED,
)

logging.basicConfig(level=logging.INFO)


async def cmd_stop_smoking(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    stop_smoking_data = get_stop_smoking_data(user_id)

    if stop_smoking_data:
        # Если пользователь уже зарегистрировал отказ, просто уведомим его
        await message.answer(
            STOP_SMOKING_ALREADY_STARTED.format(
                time=stop_smoking_data.stop_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        return

    stop_time = datetime.now()
    job_ids = schedule_messages(bot, user_id, stop_time, start_hour=9, end_hour=18)
    stop_smoking_data = {
        "time": stop_time.strftime("%Y-%m-%d %H:%M:%S"),
        "jobs": job_ids,
    }
    update_stop_smoking_data(user_id, stop_smoking_data)

    await message.answer(STOP_SMOKING_INFO)


async def cancel_stop_smoking(message: types.Message):
    user_id = message.from_user.id
    stop_smoking_data = get_stop_smoking_data(user_id)

    if stop_smoking_data:
        # Отменяем запланированные сообщения
        cancel_scheduled_messages(stop_smoking_data["jobs"])
        delete_stop_smoking_data(user_id)  # Удаляем данные отказа

        # Вычисляем время без сигарет
        stop_time = stop_smoking_data.stop_time
        time_without_smoking = datetime.now() - stop_time
        hours, remainder = divmod(time_without_smoking.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        await message.answer(
            STOP_SMOKING_CANCELLED.format(hours=int(hours), minutes=int(minutes))
        )
    else:
        await message.answer("Вы еще не регистрировали отказ от курения.")
