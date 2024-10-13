from aiogram import types
from aiogram import types, Bot
from aiogram.types import (
    ContentType,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

# from db.data_manager import get_user_data, update_user_data, get_last_relapse_session
from db.relapse import (
    RelapseSession,
    timezone,
    get_last_relapse_session,
    update_last_relapse_session,
    add_new_relapse_session,
)

from datetime import datetime
from modules.gpt_therapist import GPTTherapist
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
    new_session = {
        "user_id": user_id,
    }
    add_new_relapse_session(user_id, new_session)
    last_session = get_last_relapse_session(user_id)
    await message.answer(
        RELAPSE_QUIZ_START_MESSAGE.format(
            date_time=last_session.timestamp.strftime("%d.%m.%Y %H:%M:%S")
        ),
        reply_markup=ReplyKeyboardRemove(),
    )

    await ask_situation(message)


async def ask_situation(message: types.Message):
    user_id = message.from_user.id
    last_session = get_last_relapse_session(user_id)
    last_session.current_step = "relapse_situation"
    update_last_relapse_session(user_id, last_session)

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
    last_session = get_last_relapse_session(user_id)

    if message.text == "Свой вариант":
        last_session.current_step = "relapse_custom_situation"
        update_last_relapse_session(user_id, last_session)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_SITUATION_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        last_session.situation = message.text
        last_session.current_step = "relapse_thoughts"
        update_last_relapse_session(user_id, last_session)
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
    last_session = get_last_relapse_session(user_id)

    if message.text == "Свой вариант":
        last_session.current_step = "relapse_custom_thoughts"
        update_last_relapse_session(user_id, last_session)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_THOUGHTS_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        last_session.thoughts = message.text
        last_session.current_step = "relapse_emotions"
        update_last_relapse_session(user_id, last_session)
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
    last_session = get_last_relapse_session(user_id)
    last_session.emotion_type = message.text
    last_session.current_step = "relapse_emotion_score"
    update_last_relapse_session(user_id, last_session)

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
    last_session = get_last_relapse_session(user_id)

    try:
        emotion_score = int(message.text)
        if emotion_score < 1 or emotion_score > 5:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return

    last_session.emotion_score = emotion_score
    last_session.current_step = "relapse_physical"
    update_last_relapse_session(user_id, last_session)
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


async def handle_relapse_physical(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    last_session = get_last_relapse_session(user_id)

    if message.content_type == ContentType.VOICE:
        voice_message_id = message.voice.file_id
        last_session.physical = f"Голосовое сообщение: {voice_message_id}"
        file = await bot.get_file(voice_message_id)
        # last_session.voice_message = file.file_path
        last_session.current_step = "relapse_behavior"
        update_last_relapse_session(user_id, last_session)
        await ask_behavior(message)
        return

    if message.text == "Другое":
        last_session.current_step = "relapse_custom_physical"
        update_last_relapse_session(user_id, last_session)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_PHYSICAL_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        last_session.physical = message.text
        last_session.current_step = "relapse_behavior"
        update_last_relapse_session(user_id, last_session)
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
    last_session = get_last_relapse_session(user_id)

    if message.text == "Другое":
        last_session.current_step = "relapse_custom_behavior"
        update_last_relapse_session(user_id, last_session)
        await message.answer(
            RELAPSE_QUIZ_CUSTOM_BEHAVIOR_PROMPT, reply_markup=ReplyKeyboardRemove()
        )
    else:
        last_session.behavior = message.text
        last_session.current_step = "relapse_done"
        update_last_relapse_session(user_id, last_session)
        await finish_relapse_quiz(message)


async def finish_relapse_quiz(message: types.Message):
    user_id = message.from_user.id

    # Получаем сессию рецидива и все необходимые атрибуты до закрытия сессии
    last_session = get_last_relapse_session(user_id)

    situation = last_session.situation
    thoughts = last_session.thoughts
    emotion_type = last_session.emotion_type
    emotion_score = last_session.emotion_score
    physical = last_session.physical
    behavior = last_session.behavior

    last_session.current_step = None
    update_last_relapse_session(user_id, last_session)

    text = (
        f"📝 *Твои ответы:*\n\n"
        f"*Ситуация:* {situation}\n"
        f"*Мысли:* {thoughts}\n"
        f"*Эмоции:* {emotion_type} (Оценка: {emotion_score})\n"
        f"*Физическое состояние:* {physical}\n"
        f"*Поведение:* {behavior}\n"
    )

    await message.answer(
        RELAPSE_QUIZ_FINISH_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown",
    )

    response = GPTTherapist().get_help(text)
    await message.answer(text, parse_mode="Markdown")
    await message.answer(response, parse_mode="Markdown")


async def handle_relapse_custom_message(message: types.Message):
    user_id = message.from_user.id
    last_session = get_last_relapse_session(user_id)
    current_step = last_session.current_step

    if current_step == "relapse_custom_situation":
        last_session.situation = message.text
        last_session.current_step = "relapse_thoughts"
        update_last_relapse_session(user_id, last_session)
        await ask_thoughts(message)

    elif current_step == "relapse_custom_thoughts":
        last_session.thoughts = message.text
        last_session.current_step = "relapse_emotions"
        update_last_relapse_session(user_id, last_session)
        await ask_emotions(message)

    elif current_step == "relapse_custom_physical":
        last_session.physical = message.text
        last_session.current_step = "relapse_behavior"
        update_last_relapse_session(user_id, last_session)
        await ask_behavior(message)

    elif current_step == "relapse_custom_behavior":
        last_session.behavior = message.text
        last_session.current_step = "relapse_done"
        update_last_relapse_session(user_id, last_session)
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
    current_step = last_session.current_step

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
