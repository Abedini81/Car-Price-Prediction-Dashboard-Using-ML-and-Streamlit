import json
import os

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        # اگر فایل نیست، یه فایل جدید با کاربر admin بسازیم
        users = {
            "admin": {
                "password": "admin123",
                "role": "admin"
            }
        }
        save_users(users)
        return users
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password, role='user'):
    users = load_users()
    if username in users:
        return False, "User already exists."
    users[username] = {
        "password": password,
        "role": role
    }
    save_users(users)
    return True, "User registered successfully."

def authenticate(username, password):
    users = load_users()
    if username in users and users[username]['password'] == password:
        return True, users[username]['role']
    return False, None

def list_users():
    users = load_users()
    return list(users.keys())
