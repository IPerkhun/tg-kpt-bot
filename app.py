import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import BotCommand
from dotenv import load_dotenv

from db.data_manager import (
    get_last_relapse_session,
    get_last_start_quiz,
    get_last_voice_user_data,
)
from modules.note_manager import get_all_notes
from modules.relapse_quiz import start_relapse_quiz, handle_relapse_step
from modules.speak_emotion import start_voice_recording, handle_voice_step
from modules.start_quiz import start_quiz, handle_quiz_step
from modules.stop_smoking import cmd_stop_smoking
from utils.content import help_text
from utils.scheduler import start_scheduler


load_dotenv()

logging.basicConfig(level=logging.DEBUG)
bot = Bot(
    token=os.environ["TG_API_TOKEN"],
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
dp = Dispatcher()


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать квиз"),
        BotCommand(command="/stop_smoking", description="Бросить курить"),
        BotCommand(command="/relapse_warning", description="Я сейчас сорвусь"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/notes", description="Мои заметки"),
        BotCommand(
            command="/speak_emotion", description="Записать голосовое сообщение"
        ),
    ]
    await bot.set_my_commands(commands)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        help_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode="MArkdown"
    )


# Обработчик для команды /notes
@dp.message(Command("notes"))
async def cmd_notes(message: types.Message):
    user_id = message.from_user.id
    notes_text = get_all_notes(user_id)

    if not notes_text:
        await message.answer("У вас пока нет заметок.")
    else:
        await message.answer(
            notes_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode="Markdown"
        )


# Обработчик для команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await start_quiz(message)


@dp.message(
    lambda message: get_last_start_quiz(message.from_user.id).get("current_step")
)
async def handle_quiz(message: types.Message):
    await handle_quiz_step(message)


# Обработчики для опроса при желании сорваться /relapse_warning
@dp.message(Command("relapse_warning"))
async def cmd_relapse_warning(message: types.Message):
    await start_relapse_quiz(message)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    is not None
)
async def handle_relapse(message: types.Message):
    await handle_relapse_step(message, bot)


# Обработчик для команды /stop_smoking
@dp.message(Command("stop_smoking"))
async def stop_smoking_handler(message: types.Message):
    await cmd_stop_smoking(message, bot)


# Обработчик для команды /speak_emotion
@dp.message(Command("speak_emotion"))
async def cmd_speak_emotion(message: types.Message):
    await start_voice_recording(message)


@dp.message(
    lambda message: get_last_voice_user_data(message.from_user.id).get("current_step")
    is not None
)
async def handle_voice(message: types.Message):
    await handle_voice_step(message, bot)


async def main():
    start_scheduler()
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
