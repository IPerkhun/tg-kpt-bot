from modules.auto_messaging import schedule_messages
from db.stop_smoking import (
    get_stop_smoking_data,
    update_stop_smoking_data,
    delete_stop_smoking_data,
)
from datetime import datetime
from aiogram import types, Bot
import logging
from utils.content import (
    STOP_SMOKING_INFO,
    STOP_SMOKING_ALREADY_STARTED,
    STOP_SMOKING_CANCELLED,
)

logging.basicConfig(level=logging.INFO)
from aiogram.types import CallbackQuery


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отменить отправку сообщений",
                callback_data="cancel_stop_smoking",
            )
        ]
    ]
)


async def cmd_stop_smoking(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    stop_smoking_data = get_stop_smoking_data(user_id)

    if stop_smoking_data:
        execute_time = datetime.now() - stop_smoking_data.stop_time
        await message.answer(
            STOP_SMOKING_ALREADY_STARTED.format(
                time=stop_smoking_data.stop_time.strftime("%Y-%m-%d %H:%M"),
                execute_time=execute_time,
            ),
            reply_markup=inline_keyboard,
        )
        return

    stop_time = datetime.now()
    job_ids = schedule_messages(bot, user_id, stop_time, start_hour=9, end_hour=18)
    stop_smoking_data = {
        "time": stop_time.strftime("%Y-%m-%d %H:%M:%S"),
        "jobs": job_ids,
    }
    update_stop_smoking_data(user_id, stop_smoking_data)

    await message.answer(STOP_SMOKING_INFO, reply_markup=inline_keyboard)


async def cancel_stop_smoking(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stop_smoking_data = get_stop_smoking_data(user_id)

    if stop_smoking_data:
        delete_stop_smoking_data(user_id)

        stop_time = stop_smoking_data.stop_time
        time_without_smoking = datetime.now() - stop_time
        days, remainder = divmod(time_without_smoking.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        await callback_query.message.answer(
            STOP_SMOKING_CANCELLED.format(
                days=int(days), hours=int(hours), minutes=int(minutes)
            )
        )
        await callback_query.answer()
    else:
        await callback_query.message.answer(
            "Вы еще не регистрировали отказ от курения."
        )
