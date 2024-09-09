from modules.auto_messaging import schedule_messages, cancel_scheduled_messages
from db.data_manager import get_stop_smoking_data, update_stop_smoking_data
from datetime import datetime
from aiogram import types, Bot


async def cmd_stop_smoking(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    stop_smoking_data = get_stop_smoking_data(user_id)

    # Если есть задачи, отменяем их
    if stop_smoking_data and "jobs" in stop_smoking_data:
        cancel_scheduled_messages(stop_smoking_data["jobs"])

    # Устанавливаем новое время отказа от курения
    stop_time = datetime.now()
    job_ids = schedule_messages(bot, user_id, stop_time)

    # Объединяем время и job_ids в одно поле
    stop_smoking_data = {
        "time": stop_time.strftime("%Y-%m-%d %H:%M:%S"),
        "jobs": job_ids,
    }

    update_stop_smoking_data(user_id, stop_smoking_data)

    await message.answer(
        "Ты решил бросить курить! Я буду поддерживать тебя на этом пути и присылать сообщения с прогрессом."
    )
