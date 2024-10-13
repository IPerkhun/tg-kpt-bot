import logging
from datetime import datetime
from aiogram import types, Bot
from db.message import add_user_message, get_last_n_messages
from utils.transcribe import transcribe_audio
from modules.gpt_therapist import GPTTherapist

logging.basicConfig(level=logging.DEBUG)
gpt_therapist = GPTTherapist()


async def handle_user_text(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text

    add_user_message(
        user_id,
        {
            "type": "text",
            "content": user_message,
            "timestamp": datetime.utcnow(),
            "role": "user",
        },
    )

    context = get_last_n_messages(user_id, 5)
    reply = gpt_therapist.get_reply(f"{context}\nuser: {user_message}")

    add_user_message(
        user_id,
        {
            "type": "text",
            "content": reply,
            "timestamp": datetime.utcnow(),
            "role": "bot",
        },
    )

    await message.answer(reply)


async def handle_user_voice(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    voice_message_id = message.voice.file_id

    # Загружаем и обрабатываем голосовое сообщение
    file_info = await bot.get_file(voice_message_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)

    local_file_path = f"/tmp/{voice_message_id}.ogg"
    with open(local_file_path, "wb") as f:
        f.write(downloaded_file.getvalue())

    # Транскрибируем голосовое сообщение в текст
    transcript_text = await transcribe_audio(local_file_path)

    add_user_message(
        user_id,
        {
            "type": "voice",
            "content": transcript_text,
            "timestamp": datetime.utcnow(),
            "role": "user",
        },
    )

    context = get_last_n_messages(user_id, 5)
    reply = gpt_therapist.get_reply(f"{context}\nuser: {transcript_text}")

    add_user_message(
        user_id,
        {
            "type": "text",
            "content": reply,
            "timestamp": datetime.utcnow(),
            "role": "bot",
        },
    )

    await message.answer(reply)
