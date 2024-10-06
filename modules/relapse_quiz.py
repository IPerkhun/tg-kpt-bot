from aiogram import types
import asyncio
from aiogram import types, Bot
from aiogram.types import (
    ContentType,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from db.data_manager import get_user_data, update_user_data, get_last_relapse_session
from datetime import datetime
from utils.data_models import RelapseSession
from modules.gpt_therapist import GPTTherapist
from dataclasses import asdict
from utils.content import (
    RELAPSE_QUIZ_START_MESSAGE,
    RELAPSE_QUIZ_SITUATION_PROMPT,
    RELAPSE_QUIZ_CUSTOM_SITUATION_PROMPT,
    RELAPSE_QUIZ_THOUGHTS_PROMPT,
    RELAPSE_QUIZ_CUSTOM_THOUGHTS_PROMPT,
    RELAPSE_QUIZ_EMOTIONS_PROMPT,
    RELAPSE_QUIZ_EMOTION_SCORE_PROMPT,
    RELAPSE_QUIZ_PHYSICAL_PROMPT,
    RELAPSE_QUIZ_CUSTOM_PHYSICAL_PROMPT,
    RELAPSE_QUIZ_BEHAVIOR_PROMPT,
    RELAPSE_QUIZ_CUSTOM_BEHAVIOR_PROMPT,
    RELAPSE_QUIZ_FINISH_MESSAGE,
    RELAPSE_QUIZ_ERROR_MESSAGE,
)


async def start_relapse_quiz(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    # Создаем новую сессию
    new_session = RelapseSession(date_time=datetime.now().strftime("%d.%m.%Y %H:%M"))

    if "relapse_sessions" not in user_data:
        user_data["relapse_sessions"] = []

    user_data["relapse_sessions"].append(asdict(new_session))
    update_user_data(user_id, user_data)

    await message.answer(
        RELAPSE_QUIZ_START_MESSAGE.format(date_time=new_session.date_time),
        reply_markup=ReplyKeyboardRemove(),
    )

    await ask_situation(message)


async def ask_situation(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]
    current_session["current_step"] = "relapse_situation"

    update_user_data(user_id, user_data)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Дома")],
            [KeyboardButton(text="На работе")],
            [KeyboardButton(text="На вечеринке")],
            [KeyboardButton(text="Свой вариант")],
        ],
        resize_keyboard=True,
    )
    await message.answer(RELAPSE_QUIZ_SITUATION_PROMPT, reply_markup=keyboard)


async def handle_relapse_situation(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]

    if message.text == "Свой вариант":
        current_session["current_step"] = "relapse_custom_situation"
        update_user_data(user_id, user_data)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_SITUATION_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        current_session["situation"] = message.text
        current_session["current_step"] = "relapse_thoughts"
        update_user_data(user_id, user_data)
        await ask_thoughts(message)


async def ask_thoughts(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Я не выдержу без сигареты")],
            [
                KeyboardButton(
                    text="Я просто хочу сдаться так как не вижу в этом смысла"
                )
            ],
            [KeyboardButton(text="Сигарета поможет мне сконцентрироваться")],
            [KeyboardButton(text="Свой вариант")],
        ],
        resize_keyboard=True,
    )
    await message.answer(RELAPSE_QUIZ_THOUGHTS_PROMPT, reply_markup=keyboard)


async def handle_relapse_thoughts(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]

    if message.text == "Свой вариант":
        current_session["current_step"] = "relapse_custom_thoughts"
        update_user_data(user_id, user_data)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_THOUGHTS_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        current_session["thoughts"] = message.text
        current_session["current_step"] = "relapse_emotions"
        update_user_data(user_id, user_data)
        await ask_emotions(message)


async def ask_emotions(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Стресс")],
            [KeyboardButton(text="Тревога")],
            [KeyboardButton(text="Злость")],
            [KeyboardButton(text="Возбуждение")],
        ],
        resize_keyboard=True,
    )
    await message.answer(RELAPSE_QUIZ_EMOTIONS_PROMPT, reply_markup=keyboard)


async def handle_relapse_emotions(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]
    current_session["emotion_type"] = message.text

    current_session["current_step"] = "relapse_emotion_score"
    update_user_data(user_id, user_data)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1"),
                KeyboardButton(text="2"),
                KeyboardButton(text="3"),
                KeyboardButton(text="4"),
                KeyboardButton(text="5"),
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer(
        RELAPSE_QUIZ_EMOTION_SCORE_PROMPT.format(emotion_type=message.text),
        reply_markup=keyboard,
    )


async def handle_relapse_emotion_score(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]

    try:
        emotion_score = int(message.text)
        if emotion_score < 1 or emotion_score > 5:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return

    current_session["emotion_score"] = emotion_score

    current_session["current_step"] = "relapse_physical"
    update_user_data(user_id, user_data)
    await ask_physical(message)


async def ask_physical(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мания")],
            [KeyboardButton(text="Трясущиеся руки")],
            [KeyboardButton(text="Все окей ")],
            [KeyboardButton(text="Другое")],
        ],
        resize_keyboard=True,
    )
    await message.answer(RELAPSE_QUIZ_PHYSICAL_PROMPT, reply_markup=keyboard)


async def handle_relapse_physical(message: types.Message, bot):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]

    if message.content_type == ContentType.VOICE:
        voice_message_id = message.voice.file_id
        current_session["physical"] = f"Голосовое сообщение: {voice_message_id}"
        file = await bot.get_file(voice_message_id)
        current_session["voice_message"] = file.file_path
        current_session["current_step"] = "relapse_behavior"
        update_user_data(user_id, user_data)
        await ask_behavior(message)
        return

    if message.text == "Другое":
        current_session["current_step"] = "relapse_custom_physical"
        update_user_data(user_id, user_data)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_PHYSICAL_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        current_session["physical"] = message.text
        current_session["current_step"] = "relapse_behavior"
        update_user_data(user_id, user_data)
        await ask_behavior(message)


async def ask_behavior(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Попить чай")],
            [KeyboardButton(text="Подышать свежим воздухом")],
            [KeyboardButton(text="Набрать по телефону близкому человеку")],
            [KeyboardButton(text="Другое")],
        ],
        resize_keyboard=True,
    )
    await message.answer(RELAPSE_QUIZ_BEHAVIOR_PROMPT, reply_markup=keyboard)


async def handle_relapse_behavior(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]

    if message.text == "Другое":
        current_session["current_step"] = "relapse_custom_behavior"
        update_user_data(user_id, user_data)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_BEHAVIOR_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        current_session["behavior"] = message.text
        current_session["current_step"] = "relapse_done"
        update_user_data(user_id, user_data)
        await finish_relapse_quiz(message)


async def finish_relapse_quiz(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]
    current_session["current_step"] = None
    update_user_data(user_id, user_data)

    response = GPTTherapist().get_help(user_data["relapse_sessions"][:-1])

    await message.answer(
        RELAPSE_QUIZ_FINISH_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown",
    )

    text = (
        f"📝 *Твои ответы:*\n\n"
        f"*Ситуация:* {current_session['situation']}\n"
        f"*Мысли:* {current_session['thoughts']}\n"
        f"*Эмоции:* {current_session['emotion_type']} (Оценка: {current_session['emotion_score']})\n"
        f"*Физическое состояние:* {current_session['physical']}\n"
        f"*Поведение:* {current_session['behavior']}\n"
    )

    await message.answer(text, parse_mode="Markdown")
    await asyncio.sleep(5)
    await message.answer(response, parse_mode="Markdown")


async def handle_relapse_custom_message(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    current_session = user_data["relapse_sessions"][-1]
    current_step = current_session["current_step"]

    if current_step == "relapse_custom_situation":
        current_session["situation"] = message.text
        current_session["current_step"] = "relapse_thoughts"
        update_user_data(user_id, user_data)
        await ask_thoughts(message)

    elif current_step == "relapse_custom_thoughts":
        current_session["thoughts"] = message.text
        current_session["current_step"] = "relapse_emotions"
        update_user_data(user_id, user_data)
        await ask_emotions(message)

    elif current_step == "relapse_custom_physical":
        current_session["physical"] = message.text
        current_session["current_step"] = "relapse_behavior"
        update_user_data(user_id, user_data)
        await ask_behavior(message)

    elif current_step == "relapse_custom_behavior":
        current_session["behavior"] = message.text
        current_session["current_step"] = "relapse_done"
        update_user_data(user_id, user_data)
        await finish_relapse_quiz(message)

    else:
        await message.answer(RELAPSE_QUIZ_ERROR_MESSAGE)
        await start_relapse_quiz(message)


RELAPSE_HANDLERS_MAP = {
    "relapse_situation": handle_relapse_situation,
    "relapse_thoughts": handle_relapse_thoughts,
    "relapse_custom_situation": handle_relapse_custom_message,
    "relapse_custom_thoughts": handle_relapse_custom_message,
    "relapse_custom_physical": handle_relapse_custom_message,
    "relapse_custom_behavior": handle_relapse_custom_message,
    "relapse_emotions": handle_relapse_emotions,
    "relapse_emotion_score": handle_relapse_emotion_score,
    "relapse_physical": handle_relapse_physical,
    "relapse_behavior": handle_relapse_behavior,
}


async def handle_relapse_step(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    last_session = get_last_relapse_session(user_id)
    current_step = last_session.get("current_step")

    handler = RELAPSE_HANDLERS_MAP.get(current_step)
    if handler:
        if current_step in ["relapse_physical"]:
            await handler(message, bot)
        else:
            await handler(message)
    else:
        await message.answer(
            "handle_relapse_step - Не могу определить текущий шаг. Попробуйте снова."
        )
