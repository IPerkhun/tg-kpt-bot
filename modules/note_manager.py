from db.relapse import get_all_notes
from aiogram import types
from modules.gpt_therapist import GPTTherapist


# Функция для получения всех заметок
async def handle_notes_command(message: types.Message):
    user_id = message.from_user.id
    notes_text = get_all_notes(user_id)
    notes_text = f"""
    Ваши заметки:
    {notes_text}
    Проанализируйте их, чтобы понять, что вас беспокоит и как вы можете справиться с этим.
    Если ничего нет - попробуйте написать что-то новое.
    Если есть - попробуйте найти закономерности и понять, что толкает на рецидив.
    """
    response = GPTTherapist().get_reply(notes_text)
    if not notes_text:
        await message.answer("У вас пока нет заметок.")
    else:
        await message.answer(
            notes_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode="Markdown"
        )
