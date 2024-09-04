from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db.data_manager import get_user_data, update_user_data, clear_user_data
from utils.content import (
    WELCOME_MESSAGE, STEP1_CIGARETTES_MESSAGE, STEP1_ELECTRONIC_MESSAGE, 
    STEP1_HOOKAH_MESSAGE, STEP1_IQOS_MESSAGE, STEP2_MESSAGE, 
    STEP3_MESSAGE, CUSTOM_REASON_PROMPT, FINISH_QUIZ_MESSAGE
)


async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    user_data['current_step'] = 'step1'
    update_user_data(user_id, user_data)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сигареты")],
            [KeyboardButton(text="Электронная сигарета или HQD")],
            [KeyboardButton(text="Кальян")],
            [KeyboardButton(text="Айкос")]
        ],
        resize_keyboard=True
    )
    await message.answer(WELCOME_MESSAGE, reply_markup=keyboard, parse_mode='Markdown')

async def handle_quiz_step1(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    user_data['smoking_type'] = message.text
    user_data['current_step'] = 'step2'
    update_user_data(user_id, user_data)

    if message.text == "Сигареты":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="До 5 штук в день 😌")],
                [KeyboardButton(text="До 10, но держусь 😬")],
                [KeyboardButton(text="Больше 15, это уже серьезно 😅")],
                [KeyboardButton(text="Целая пачка и больше в день 🚬")]
            ],
            resize_keyboard=True
        )
        await message.answer(STEP1_CIGARETTES_MESSAGE, reply_markup=keyboard)
    
    elif message.text == "Электронная сигарета или HQD":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Заряжаюсь утром или вечером ⚡️")],
                [KeyboardButton(text="Дымлю каждые 2-3 часа ⏰")],
                [KeyboardButton(text="Электронка всегда со мной, каждые 20-30 минут 🔋")]
            ],
            resize_keyboard=True
        )
        await message.answer(STEP1_ELECTRONIC_MESSAGE, reply_markup=keyboard)
    
    elif message.text == "Кальян":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Только по выходным 🌴")],
                [KeyboardButton(text="2-3 раза в неделю 😎")],
                [KeyboardButton(text="Каждый день, без кальяна никуда 💨")]
            ],
            resize_keyboard=True
        )
        await message.answer(STEP1_HOOKAH_MESSAGE, reply_markup=keyboard)
    
    elif message.text == "Айкос":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Менее 5")],
                [KeyboardButton(text="Менее 10")],
                [KeyboardButton(text="Более 15")],
                [KeyboardButton(text="1 пачка и более в день")]
            ],
            resize_keyboard=True
        )
        await message.answer(STEP1_IQOS_MESSAGE, reply_markup=keyboard)

async def handle_quiz_step2(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    user_data['intensity'] = message.text
    user_data['current_step'] = 'step3'
    update_user_data(user_id, user_data)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Меньше года")],
            [KeyboardButton(text="1-3 года")],
            [KeyboardButton(text="5-10 лет")],
            [KeyboardButton(text="Более 10 лет")]
        ],
        resize_keyboard=True
    )
    await message.answer(STEP2_MESSAGE, reply_markup=keyboard)

async def handle_quiz_step3(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    user_data['period'] = message.text
    user_data['current_step'] = 'step4'
    update_user_data(user_id, user_data)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Здоровье")],
            [KeyboardButton(text="Финансы")],
            [KeyboardButton(text="Социальное окружение")],
            [KeyboardButton(text="Свой вариант")]
        ],
        resize_keyboard=True
    )
    await message.answer(STEP3_MESSAGE, reply_markup=keyboard)

async def handle_quiz_step4(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if message.text == "Свой вариант":
        user_data['current_step'] = 'custom_reason'
        update_user_data(user_id, user_data)
        await message.answer(CUSTOM_REASON_PROMPT, reply_markup=ReplyKeyboardRemove())
    else:
        user_data['reason'] = message.text
        await finish_quiz(message)

async def handle_custom_reason(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    user_data['reason'] = message.text
    update_user_data(user_id, user_data)
    await finish_quiz(message)

async def finish_quiz(message: types.Message):
    user_id = message.from_user.id
    # clear_user_data(user_id)  # Очищаем данные после завершения квиза
    user_data = get_user_data(user_id)
    user_data['current_step'] = None
    update_user_data(user_id, user_data)

    await message.answer(FINISH_QUIZ_MESSAGE, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
