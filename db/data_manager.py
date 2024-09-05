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
    return data.get(str(user_id), {"relapse_sessions": []})

def get_last_relapse_session(user_id):
    user_data = get_user_data(user_id)
    if user_data["relapse_sessions"]:
        return user_data["relapse_sessions"][-1]
    user_data["relapse_sessions"].append({})
    return user_data["relapse_sessions"][-1]

def update_user_data(user_id, user_data):
    data = load_data()
    data[str(user_id)] = user_data
    save_data(data)

def clear_user_data(user_id):
    data = load_data()
    if str(user_id) in data:
        del data[str(user_id)]
    save_data(data)

def get_stop_smoking_time(user_id):
    user_data = get_user_data(user_id)
    return user_data.get('stop_smoking_time')