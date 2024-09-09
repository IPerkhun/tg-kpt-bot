from aiogram import types, Bot
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    ContentType,
)
from db.data_manager import (
    get_last_voice_user_data,
    update_last_voice_user_data,
    get_user_data,
    update_user_data,
)
from modules.transcribe import transcribe_audio
from utils.data_models import VoiceData
from dataclasses import asdict


# Функция для старта сценария записи голосового сообщения
async def start_voice_recording(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    last_voice_data = VoiceData()
    last_voice_data.current_step = "waiting_for_voice"

    # # Проверяем, что пользователь не начал запись голосового сообщения
    # if last_voice_data and not last_voice_data["confirmed"]:
    #     await message.answer(
    #         "Пожалуйста, подтвердите или перезапишите предыдущее голосовое сообщение."
    #     )
    #     return

    # Обновляем данные пользователя
    user_data["voices"].append(asdict(last_voice_data))
    update_user_data(user_id, user_data)

    # Сообщение пользователю о начале записи
    await message.answer(
        "Пожалуйста, запишите голосовое сообщение, описывающее ваши текущие эмоции.",
        reply_markup=ReplyKeyboardRemove(),
    )


# Функция для обработки голосового сообщения
async def handle_voice_message(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    last_voice_data = get_last_voice_user_data(user_id)

    if message.content_type == ContentType.VOICE:
        voice_message_id = message.voice.file_id

        # Получаем файл голосового сообщения с сервера Telegram
        file_info = await bot.get_file(voice_message_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)

        # Сохраняем файл временно на сервере
        local_file_path = f"/tmp/{voice_message_id}.ogg"
        with open(local_file_path, "wb") as f:
            f.write(downloaded_file.getvalue())

        # Отправляем файл в Whisper для транскрибации
        transcript_text = await transcribe_audio(local_file_path)

        # Сохраняем данные в last_voice_user_data
        data = {
            "file_id": voice_message_id,
            "text": transcript_text,
            "confirmed": False,
            "current_step": "waiting_for_confirmation",
        }
        last_voice_data.update(data)
        update_last_voice_user_data(user_id, last_voice_data)

        # Предлагаем пользователю подтвердить текст или перезаписать
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Подтвердить")],
                [KeyboardButton(text="Перезаписать")],
            ],
            resize_keyboard=True,
        )
        await message.answer(
            f"Вот, что я услышал: \n\n'{transcript_text}'", reply_markup=keyboard
        )


# Функция для обработки подтверждения или перезаписи
async def handle_confirmation(message: types.Message):
    user_id = message.from_user.id
    last_voice_data = get_last_voice_user_data(user_id)

    if message.text == "Подтвердить":
        last_voice_data["confirmed"] = True
        last_voice_data["current_step"] = "finished"
        update_last_voice_user_data(user_id, last_voice_data)
        await message.answer(
            "Спасибо за подтверждение!", reply_markup=ReplyKeyboardRemove()
        )

    elif message.text == "Перезаписать":
        last_voice_data["confirmed"] = False
        last_voice_data["current_step"] = "waiting_for_voice"
        update_last_voice_user_data(user_id, last_voice_data)
        await start_voice_recording(message)
    else:
        await message.answer(
            "Пожалуйста, воспользуйтесь кнопками для подтверждения или перезаписи."
        )
