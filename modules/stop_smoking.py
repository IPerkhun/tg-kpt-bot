from aiogram import Bot
from db.data_manager import get_user_data, update_user_data
from aiogram import types
from modules.auto_messaging import schedule_messages
from datetime import datetime

# Функция для обработки команды /stop_smoking
async def cmd_stop_smoking(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    
    stop_time = datetime.now()
    user_data['stop_smoking_time'] = stop_time.strftime('%Y-%m-%d %H:%M:%S')
    update_user_data(user_id, user_data)
    schedule_messages(bot, user_id, stop_time)

    await message.answer(
        "Ты решил бросить курить! Я буду поддерживать тебя на этом пути и присылать сообщения с прогрессом."
    )
