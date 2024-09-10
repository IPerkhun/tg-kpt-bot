from db.data_manager import get_user_data


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
