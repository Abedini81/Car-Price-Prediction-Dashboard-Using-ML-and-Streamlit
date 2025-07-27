import json
import os

USERS_FILE = "users.json"
CURRENT_USER_FILE = "current_user.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return {"username": username, "role": user["role"]}
    return None

def login_user(user_data):
    with open(CURRENT_USER_FILE, "w") as f:
        json.dump(user_data, f)

def logout_user():
    if os.path.exists(CURRENT_USER_FILE):
        os.remove(CURRENT_USER_FILE)

def get_current_user():
    if os.path.exists(CURRENT_USER_FILE):
        with open(CURRENT_USER_FILE, "r") as f:
            return json.load(f)
    return None

def register_user(username, password):
    users = load_users()
    if any(user["username"] == username for user in users):
        return False  # Username already exists
    users.append({"username": username, "password": password, "role": "user"})  # default role: user
    save_users(users)
    return True
