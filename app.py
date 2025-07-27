import auth
import user_panel
import json

def main():
    print("Welcome to Vehicle Price Prediction System")
    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        success, role = auth.authenticate(username, password)
        if success:
            print(f"Login successful! Role: {role}")
            if role == 'admin':
                user_panel.admin_panel(username)
            else:
                user_panel.user_panel(username)
        else:
            print("Login failed. Try again.")

        again = input("Do you want to login again? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()


def save_session(username, role):
    with open('current_user.json', 'w') as f:
        json.dump({"username": username, "role": role}, f)
