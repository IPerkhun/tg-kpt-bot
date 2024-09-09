from modules.auto_messaging import schedule_messages, cancel_scheduled_messages
from db.data_manager import get_user_data, update_user_data
from datetime import datetime
from aiogram import types, Bot

async def cmd_stop_smoking(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    # Если у пользователя есть активные задачи, отменяем их
    if 'job_ids' in user_data:
        cancel_scheduled_messages(user_data['job_ids'])
    
    # Устанавливаем новое время отказа от курения
    stop_time = datetime.now()
    user_data['stop_smoking_time'] = stop_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Планируем новые напоминания и сохраняем job_ids
    job_ids = schedule_messages(bot, user_id, stop_time)
    user_data['job_ids'] = job_ids
    update_user_data(user_id, user_data)

    await message.answer(
        "Ты решил бросить курить! Я буду поддерживать тебя на этом пути и присылать сообщения с прогрессом."
    )
