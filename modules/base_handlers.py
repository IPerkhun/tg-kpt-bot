import logging
from datetime import datetime
from aiogram import types, Bot
from db.pg_manager import add_user_message, get_user_messages
from utils.transcribe import transcribe_audio
from modules.gpt_therapist import GPTTherapist

logging.basicConfig(level=logging.DEBUG)
gpt_therapist = GPTTherapist()


def get_last_n_messages(user_id: int, n: int = 5) -> str:
    """Получить последние N сообщений пользователя в формате контекста для GPT"""
    last_messages = get_user_messages(user_id)[-n:]
    context = "\n".join(
        [
            f"{msg.role}: {msg.content}"
            for msg in last_messages
            if msg.role in ["user", "bot"]
        ]
    )
    return context


async def handle_user_text(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text

    # Сохраняем текстовое сообщение пользователя в базу данных
    add_user_message(
        user_id,
        {
            "type": "text",
            "content": user_message,
            "timestamp": datetime.utcnow(),
            "role": "user",
        },
    )

    # Получаем последние N сообщений для контекста
    context = get_last_n_messages(user_id, 5)

    # Генерируем ответ от GPT
    reply = gpt_therapist.get_reply(f"{context}\nuser: {user_message}")

    # Сохраняем ответ бота в базу данных
    add_user_message(
        user_id,
        {
            "type": "text",
            "content": reply,
            "timestamp": datetime.utcnow(),
            "role": "bot",
        },
    )

    # Отправляем ответ пользователю
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

    # Сохраняем транскрибированное голосовое сообщение в базу данных
    add_user_message(
        user_id,
        {
            "type": "voice",
            "content": transcript_text,
            "timestamp": datetime.utcnow(),
            "role": "user",
        },
    )

    # Получаем последние N сообщений для контекста
    context = get_last_n_messages(user_id, 5)

    # Генерируем ответ от GPT
    reply = gpt_therapist.get_reply(f"{context}\nuser: {transcript_text}")

    # Сохраняем ответ бота в базу данных
    add_user_message(
        user_id,
        {
            "type": "text",
            "content": reply,
            "timestamp": datetime.utcnow(),
            "role": "bot",
        },
    )

    # Отправляем ответ пользователю
    await message.answer(reply)
