import asyncio
import os, logging

from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import BotCommand
from dotenv import load_dotenv

from db.base import test_db_connection, create_tables

from modules.base_handlers import handle_user_text, handle_user_voice
from modules.note_manager import handle_notes_command
from modules.relapse_quiz import (
    start_relapse_quiz,
    handle_relapse_step,
    get_last_relapse_session,
)
from modules.start_quiz import start_quiz, handle_quiz_step, get_last_start_quiz
from modules.stop_smoking import cmd_stop_smoking
from modules.gpt_therapist import GPTTherapist

from utils.content import help_text, welcome_text
from utils.scheduler import start_scheduler


load_dotenv()

logger = logging.basicConfig(level=logging.DEBUG)
dp = Dispatcher()
router = Router()  # Создаем Router


gpt_therapist = GPTTherapist(api_key=os.getenv("OPENAI_API_KEY"))
bot = Bot(
    token=os.environ["TG_API_TOKEN"],
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать квиз"),
        BotCommand(command="/start_quiz", description="Начать квиз"),
        BotCommand(command="/stop_smoking", description="Бросить курить"),
        BotCommand(command="/relapse_warning", description="Я сейчас сорвусь"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/notes", description="Мои заметки"),
    ]
    await bot.set_my_commands(commands)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        help_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode="MArkdown"
    )


from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пройти квиз", callback_data="/start_quiz")]
        ]
    )
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")


async def start_quiz_handler(message: types.Message, user_id: int = None):
    await start_quiz(message, user_id=user_id)


# Обработчик для команды /start_quiz
@dp.message(Command("start_quiz"))
async def cmd_start_quiz_message(message: types.Message):
    await start_quiz_handler(message)


# Обработчик для нажатия на кнопку с callback_data="start_quiz"
@router.callback_query(lambda c: c.data == "/start_quiz")
async def cmd_start_quiz_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await start_quiz_handler(callback_query.message, callback_query.from_user.id)


@dp.message(Command("notes"))
async def cmd_notes(message: types.Message):
    await handle_notes_command(message)  # Используем обработчик из note_manager


# Обработчики для опроса при желании сорваться /relapse_warning
@dp.message(Command("relapse_warning"))
async def cmd_relapse_warning(message: types.Message):
    await start_relapse_quiz(message)


# Обработчик для команды /stop_smoking
@dp.message(Command("stop_smoking"))
async def stop_smoking_handler(message: types.Message):
    await cmd_stop_smoking(message, bot)


@dp.message(
    lambda message: message.content_type == types.ContentType.TEXT
    and not message.text.startswith("/")
)
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # Получаем последнюю сессию рецидива и квиз
    last_quiz = get_last_start_quiz(user_id)
    last_relapse = get_last_relapse_session(user_id)

    # Проверка активности квиза или сессии рецидива
    if last_quiz and last_quiz.current_step not in [None, "finished"]:
        await handle_quiz_step(message)
    elif last_relapse and last_relapse.current_step is not None:
        await handle_relapse_step(message, bot)
    else:
        # Если квиза и сессии рецидива нет, обрабатываем как обычное сообщение
        await handle_user_text(message)


# Обработчик для голосовых сообщений
@dp.message(lambda message: message.content_type == types.ContentType.VOICE)
async def handle_voice_message(message: types.Message):
    await handle_user_voice(message, bot)


from db.feedback import add_feedback


@dp.message(Command("feedback"))
async def cmd_feedback(message: types.Message):
    user_id = message.from_user.id
    # Удаляем команду "/feedback" и любые лишние пробелы, чтобы оставить только текст отзыва
    feedback_text = message.text.removeprefix("/feedback").strip()

    if feedback_text:
        add_feedback(user_id, feedback_text)
        await message.answer("Спасибо за ваш фидбэк!")
    else:
        await message.answer(
            "Пожалуйста, отправьте свой отзыв после команды /feedback."
        )


dp.include_router(router)


async def main():
    create_tables()
    start_scheduler()
    await set_bot_commands(bot)

    try:
        test_db_connection()
    except Exception as e:
        logging.error(f"Database connection error: {e}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
