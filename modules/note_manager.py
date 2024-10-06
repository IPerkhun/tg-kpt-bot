from db.data_manager import get_user_data
from aiogram import types


# Функция для получения всех заметок
def get_all_notes(user_id):
    user_data = get_user_data(user_id)
    sessions = user_data.get("relapse_sessions", [])

    if not sessions:
        return None

    notes_text = ""
    for idx, session in enumerate(sessions, 1):
        notes_text += f"📄 *Заметка {idx}*\n"
        notes_text += f"🗓 *Дата*: {session.get('date_time', 'Не указана')}\n"
        notes_text += f"📍 *Ситуация*: {session.get('situation', 'Не указана')}\n"
        notes_text += f"💭 *Мысли*: {session.get('thoughts', 'Не указаны')}\n"
        notes_text += f"😶‍🌫️ *Эмоции*: {session.get('emotion_type', 'Не указаны')} (Оценка: {session.get('emotion_score', 'Не указана')})\n"
        notes_text += (
            f"💪 *Физическое состояние*: {session.get('physical', 'Не указано')}\n"
        )
        notes_text += f"🎯 *Поведение*: {session.get('behavior', 'Не указано')}\n"
        notes_text += f"{'-'*30}\n\n"

    return notes_text


# Функция для обработки команды /notes
async def handle_notes_command(message: types.Message):
    user_id = message.from_user.id
    notes_text = get_all_notes(user_id)

    if not notes_text:
        await message.answer("У вас пока нет заметок.")
    else:
        await message.answer(
            notes_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode="Markdown"
        )
