import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from aiogram.enums import ParseMode

from modules.start_quiz import (
    start_quiz,
    handle_quiz_step1,
    handle_quiz_step2,
    handle_quiz_step3,
    handle_quiz_step4,
    handle_custom_reason,
)

from modules.relapse_quiz import (
    start_relapse_quiz,
    handle_relapse_situation,
    handle_relapse_thoughts,
    handle_relapse_custom_message,
    handle_relapse_emotions,
    handle_relapse_emotion_score,
    handle_relapse_physical,
    handle_relapse_behavior,
)

from modules.speak_emotion import (
    start_voice_recording,
    handle_voice_message,
    handle_confirmation,
)
from modules.stop_smoking import cmd_stop_smoking
from modules.note_manager import get_all_notes
from db.data_manager import get_last_relapse_session, get_last_start_quiz
from utils.content import help_text
from utils.scheduler import start_scheduler

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
bot = Bot(
    token=os.environ["TG_API_TOKEN"],
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN,
    ),
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


# Обработчики для этапов квиза
@dp.message(
    lambda message: get_last_start_quiz(message.from_user.id).get("current_step")
    == "step1"
)
async def handle_quiz_1(message: types.Message):
    await handle_quiz_step1(message)


@dp.message(
    lambda message: get_last_start_quiz(message.from_user.id).get("current_step")
    == "step2"
)
async def handle_quiz_2(message: types.Message):
    await handle_quiz_step2(message)


@dp.message(
    lambda message: get_last_start_quiz(message.from_user.id).get("current_step")
    == "step3"
)
async def handle_quiz_3(message: types.Message):
    await handle_quiz_step3(message)


@dp.message(
    lambda message: get_last_start_quiz(message.from_user.id).get("current_step")
    == "step4"
)
async def handle_quiz_4(message: types.Message):
    await handle_quiz_step4(message)


@dp.message(
    lambda message: get_last_start_quiz(message.from_user.id).get("current_step")
    == "custom_reason_start_quiz"
)
async def handle_quiz_custom_reason(message: types.Message):
    await handle_custom_reason(message)


# Обработчики для опроса при желании сорваться /relapse_warning
@dp.message(Command("relapse_warning"))
async def cmd_relapse_warning(message: types.Message):
    await start_relapse_quiz(message)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    == "relapse_situation"
)
async def handle_relapse_2(message: types.Message):
    await handle_relapse_situation(message)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    == "relapse_thoughts"
)
async def handle_relapse_3(message: types.Message):
    await handle_relapse_thoughts(message)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    in [
        "relapse_custom_situation",
        "relapse_custom_thoughts",
        "relapse_custom_physical",
        "relapse_custom_behavior",
    ]
)
async def handle_custom_message(message: types.Message):
    await handle_relapse_custom_message(message)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    == "relapse_emotions"
)
async def handle_relapse_4(message: types.Message):
    await handle_relapse_emotions(message)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    == "relapse_emotion_score"
)
async def handle_relapse_5_score(message: types.Message):
    await handle_relapse_emotion_score(message)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    == "relapse_physical"
)
async def handle_relapse_5(message: types.Message):
    await handle_relapse_physical(message, bot)


@dp.message(
    lambda message: get_last_relapse_session(message.from_user.id).get("current_step")
    == "relapse_behavior"
)
async def handle_relapse_6(message: types.Message):
    await handle_relapse_behavior(message)


# Обработчик для команды /stop_smoking
@dp.message(Command("stop_smoking"))
async def stop_smoking_handler(message: types.Message):
    await cmd_stop_smoking(message, bot)


# Обработчик для команды /speak_emotion
@dp.message(Command("speak_emotion"))
async def cmd_speak_emotion(message: types.Message):
    await start_voice_recording(message)


from db.data_manager import get_last_voice_user_data


@dp.message(
    lambda message: get_last_voice_user_data(message.from_user.id).get("current_step")
    == "waiting_for_voice"
)
async def handle_voice_input(message: types.Message):
    await handle_voice_message(message, bot)


@dp.message(
    lambda message: get_last_voice_user_data(message.from_user.id).get("current_step")
    == "waiting_for_confirmation"
)
async def handle_voice_confirmation(message: types.Message):
    await handle_confirmation(message)


async def main():
    start_scheduler()
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
