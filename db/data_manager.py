import json
import os

# Файл для хранения данных
DATA_FILE = "user_data.json"

# --- Основные функции для работы с данными пользователя ---


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_user_data(user_id) -> dict:
    """Получить данные пользователя или инициализировать новую структуру данных"""
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {
            "relapse_sessions": [],
            "voices": [],
            "start_quizes": [],
            "stop_smoking_data": {},
        }
        save_data(data)
    return data[str(user_id)]


def update_user_data(user_id, user_data):
    """Обновить данные пользователя"""
    data = load_data()
    data[str(user_id)] = user_data
    save_data(data)


def clear_user_data(user_id):
    """Очистить данные пользователя"""
    data = load_data()
    if str(user_id) in data:
        del data[str(user_id)]
    save_data(data)


# --- Управление голосовыми сообщениями ---


def get_voice_user_data(user_id):
    """Получить все голосовые сообщения пользователя"""
    user_data = get_user_data(user_id)
    return user_data.get("voices", [])


def update_voice_user_data(user_id, voices):
    """Обновить список голосовых сообщений пользователя"""
    user_data = get_user_data(user_id)
    user_data["voices"] = voices
    update_user_data(user_id, user_data)


def update_last_voice_user_data(user_id, voice_data):
    """Обновить последнее голосовое сообщение пользователя"""
    voices = get_voice_user_data(user_id)
    if voices:
        voices[-1] = voice_data
    update_voice_user_data(user_id, voices)


def get_last_voice_user_data(user_id):
    """Получить последнее голосовое сообщение пользователя"""
    voices = get_voice_user_data(user_id)
    if voices:
        return voices[-1]
    return {"current_step": None}


# --- Управление данными отказа от курения ---


def get_stop_smoking_data(user_id):
    """Получить данные отказа от курения для пользователя"""
    user_data = get_user_data(user_id)
    return user_data.get("stop_smoking_data", {})


def update_stop_smoking_data(user_id, stop_smoking_data):
    """Обновить данные отказа от курения для пользователя"""
    user_data = get_user_data(user_id)
    user_data["stop_smoking_data"] = stop_smoking_data
    update_user_data(user_id, user_data)


# --- Управление данными рецидивов ---


def get_relapse_sessions(user_id):
    """Получить все сессии рецидива для пользователя"""
    user_data = get_user_data(user_id)
    return user_data.get("relapse_sessions", [])


def update_relapse_sessions(user_id, relapse_sessions):
    """Обновить список сессий рецидива для пользователя"""
    user_data = get_user_data(user_id)
    user_data["relapse_sessions"] = relapse_sessions
    update_user_data(user_id, user_data)


def get_last_relapse_session(user_id):
    """Получить последнюю сессию рецидива для пользователя"""
    relapse_sessions = get_relapse_sessions(user_id)
    if relapse_sessions:
        return relapse_sessions[-1]
    return {"current_step": None}


def update_last_relapse_session(user_id, relapse_session):
    """Обновить последнюю сессию рецидива пользователя"""
    relapse_sessions = get_relapse_sessions(user_id)
    if relapse_sessions:
        relapse_sessions[-1] = relapse_session
    update_relapse_sessions(user_id, relapse_sessions)


# --- Управление данными квизов ---


def get_last_start_quiz(user_id):
    """Получить последний квиз пользователя"""
    user_data = get_user_data(user_id)
    if user_data["start_quizes"]:
        return user_data["start_quizes"][-1]
    return {"current_step": None}


def update_last_start_quiz(user_id, quiz_data):
    """Обновить последний квиз пользователя"""
    user_data = get_user_data(user_id)
    if user_data["start_quizes"]:
        user_data["start_quizes"][-1] = quiz_data
    update_user_data(user_id, user_data)
