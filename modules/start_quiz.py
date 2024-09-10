from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db.data_manager import (
    get_last_start_quiz,
    update_last_start_quiz,
    get_user_data,
    update_user_data,
)
from utils.content import (
    WELCOME_MESSAGE,
    STEP1_CIGARETTES_MESSAGE,
    STEP1_ELECTRONIC_MESSAGE,
    STEP1_HOOKAH_MESSAGE,
    STEP1_IQOS_MESSAGE,
    STEP2_MESSAGE,
    STEP3_MESSAGE,
    CUSTOM_REASON_PROMPT,
    FINISH_QUIZ_MESSAGE,
)
from utils.data_models import StartQuiz


# Старт квиза и добавление пустой записи в start_quizes
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    # Добавляем новый пустой квиз
    new_quiz = StartQuiz().to_dict()
    new_quiz["current_step"] = "step1"
    user_data = get_user_data(user_id)
    user_data["start_quizes"].append(new_quiz)
    update_user_data(user_id, user_data)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сигареты")],
            [KeyboardButton(text="Электронная сигарета или HQD")],
            [KeyboardButton(text="Кальян")],
            [KeyboardButton(text="Айкос")],
        ],
        resize_keyboard=True,
    )
    await message.answer(WELCOME_MESSAGE, reply_markup=keyboard, parse_mode="Markdown")


# Обработка первого шага (выбор типа курения)
async def handle_quiz_step1(message: types.Message):
    user_id = message.from_user.id
    last_quiz = get_last_start_quiz(user_id)

    last_quiz["smoking_type"] = message.text
    last_quiz["current_step"] = "step2"
    update_last_start_quiz(user_id, last_quiz)

    if message.text == "Сигареты":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="До 5 штук в день 😌")],
                [KeyboardButton(text="До 10, но держусь 😬")],
                [KeyboardButton(text="Больше 15, это уже серьезно 😅")],
                [KeyboardButton(text="Целая пачка и больше в день 🚬")],
            ],
            resize_keyboard=True,
        )
        await message.answer(STEP1_CIGARETTES_MESSAGE, reply_markup=keyboard)

    elif message.text == "Электронная сигарета или HQD":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Заряжаюсь утром или вечером ⚡️")],
                [KeyboardButton(text="Дымлю каждые 2-3 часа ⏰")],
                [
                    KeyboardButton(
                        text="Электронка всегда со мной, каждые 20-30 минут 🔋"
                    )
                ],
            ],
            resize_keyboard=True,
        )
        await message.answer(STEP1_ELECTRONIC_MESSAGE, reply_markup=keyboard)

    elif message.text == "Кальян":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Только по выходным 🌴")],
                [KeyboardButton(text="2-3 раза в неделю 😎")],
                [KeyboardButton(text="Каждый день, без кальяна никуда 💨")],
            ],
            resize_keyboard=True,
        )
        await message.answer(STEP1_HOOKAH_MESSAGE, reply_markup=keyboard)

    elif message.text == "Айкос":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Менее 5")],
                [KeyboardButton(text="Менее 10")],
                [KeyboardButton(text="Более 15")],
                [KeyboardButton(text="1 пачка и более в день")],
            ],
            resize_keyboard=True,
        )
        await message.answer(STEP1_IQOS_MESSAGE, reply_markup=keyboard)


# Обработка второго шага (интенсивность)
async def handle_quiz_step2(message: types.Message):
    user_id = message.from_user.id
    last_quiz = get_last_start_quiz(user_id)

    last_quiz["intensity"] = message.text
    last_quiz["current_step"] = "step3"
    update_last_start_quiz(user_id, last_quiz)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Меньше года")],
            [KeyboardButton(text="1-3 года")],
            [KeyboardButton(text="5-10 лет")],
            [KeyboardButton(text="Более 10 лет")],
        ],
        resize_keyboard=True,
    )
    await message.answer(STEP2_MESSAGE, reply_markup=keyboard)


# Обработка третьего шага (стаж курения)
async def handle_quiz_step3(message: types.Message):
    user_id = message.from_user.id
    last_quiz = get_last_start_quiz(user_id)

    last_quiz["period"] = message.text
    last_quiz["current_step"] = "step4"
    update_last_start_quiz(user_id, last_quiz)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Хочу выглядеть моложе и свежее 🌟")],
            [KeyboardButton(text="Надоело кашлять и задыхаться 🤒")],
            [KeyboardButton(text="Не хочу чтобы от меня воняло 🚫👃")],
            [KeyboardButton(text="Свой вариант ✍️")],
        ],
        resize_keyboard=True,
    )
    await message.answer(STEP3_MESSAGE, reply_markup=keyboard)


# Обработка четвертого шага (причина отказа от курения)
async def handle_quiz_step4(message: types.Message):
    user_id = message.from_user.id
    last_quiz = get_last_start_quiz(user_id)

    if message.text == "Свой вариант ✍️":
        last_quiz["current_step"] = "custom_reason_start_quiz"
        await message.answer(CUSTOM_REASON_PROMPT, reply_markup=ReplyKeyboardRemove())
    else:
        last_quiz["reason"] = message.text
        last_quiz["current_step"] = "finished"
        update_last_start_quiz(user_id, last_quiz)
        await finish_quiz(message)


# Обработка пользовательской причины отказа от курения
async def handle_custom_reason(message: types.Message):
    user_id = message.from_user.id
    last_quiz = get_last_start_quiz(user_id)
    last_quiz["reason"] = message.text
    update_last_start_quiz(user_id, last_quiz)
    await finish_quiz(message)


# Завершение квиза
async def finish_quiz(message: types.Message):
    user_id = message.from_user.id

    last_quiz = get_last_start_quiz(user_id)

    last_quiz["current_step"] = "finished"
    update_last_start_quiz(user_id, last_quiz)

    await message.answer(
        FINISH_QUIZ_MESSAGE, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown"
    )
