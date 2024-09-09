import json
import os

DATA_FILE = "user_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_user_data(user_id):
    data = load_data()
    if str(user_id) not in data:
        # Инициализируем пользователя с новой структурой данных
        data[str(user_id)] = {
            "relapse_sessions": [],
            "voices": [],
            "start_quizes": [],
            "stop_smoking_data": {},
        }
        save_data(data)
    return data[str(user_id)]


def get_last_relapse_session(user_id):
    user_data = get_user_data(user_id)
    if user_data["relapse_sessions"]:
        return user_data["relapse_sessions"][-1]
    return None


def get_last_start_quiz(user_id):
    user_data = get_user_data(user_id)
    if user_data["start_quizes"]:
        return user_data["start_quizes"][-1]
    return None


def update_start_quiz(user_id, quiz_data):
    user_data = get_user_data(user_id)
    user_data["start_quizes"][-1] = quiz_data
    update_user_data(user_id, user_data)


def update_user_data(user_id, user_data):
    data = load_data()
    data[str(user_id)] = user_data
    save_data(data)


def add_start_quiz(user_id, quiz_data):
    user_data = get_user_data(user_id)
    user_data["start_quizes"].append(quiz_data)
    update_user_data(user_id, user_data)


def clear_user_data(user_id):
    data = load_data()
    if str(user_id) in data:
        del data[str(user_id)]
    save_data(data)


def get_voice_user_data(user_id):
    user_data = get_user_data(user_id)
    return user_data.get("voices", [])


def update_voice_user_data(user_id, voices):
    user_data = get_user_data(user_id)
    user_data["voices"] = voices
    update_user_data(user_id, user_data)


def get_last_voice_user_data(user_id):
    if get_voice_user_data(user_id):
        return get_voice_user_data(user_id)[-1]
    return None


def update_last_voice_user_data(user_id, voice_data):
    voices = get_voice_user_data(user_id)
    voices[-1] = voice_data
    update_voice_user_data(user_id, voices)


# Методы для работы с данными отказа от курения (stop_smoking_data)
def get_stop_smoking_data(user_id):
    user_data = get_user_data(user_id)
    return user_data.get("stop_smoking_data", {})


def update_stop_smoking_data(user_id, stop_smoking_data):
    user_data = get_user_data(user_id)
    user_data["stop_smoking_data"] = stop_smoking_data
    update_user_data(user_id, user_data)
