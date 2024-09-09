from modules.auto_messaging import schedule_messages, cancel_scheduled_messages
from db.data_manager import get_user_data, update_user_data
from datetime import datetime
from aiogram import types, Bot
import json


async def cmd_stop_smoking(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    # Если у пользователя есть данные о курении, отменяем старые задачи
    if 'stop_smoking_data' in user_data:
        stop_smoking_data = user_data['stop_smoking_data']
        if 'jobs' in stop_smoking_data:
            cancel_scheduled_messages(stop_smoking_data['jobs'])
    
    # Устанавливаем новое время отказа от курения
    stop_time = datetime.now()
    job_ids = schedule_messages(bot, user_id, stop_time)

    # Объединяем время и job_ids в одно поле
    stop_smoking_data = {
        "time": stop_time.strftime('%Y-%m-%d %H:%M:%S'),
        "jobs": job_ids  
    }

    user_data['stop_smoking_data'] = stop_smoking_data
    update_user_data(user_id, user_data)

    await message.answer(
        "Ты решил бросить курить! Я буду поддерживать тебя на этом пути и присылать сообщения с прогрессом."
    )