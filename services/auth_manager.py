
import json
import os
from models.user import User

class AuthManager:
    def __init__(self, users_store, session_path="data/session.json"):
        self.users_store = users_store
        self.session_path = session_path

    def register(self, username, password):
        users = self.users_store.load()

        if any(u["username"] ==username for u in users):
            raise ValueError(f"Username '{username}' is already taken.")
        
        if not password or len(password) < 4:
            raise ValueError("Password must be at least 4 characters.")

        hashed, salt = User.hash_password(password)
        new_id = self.users_store.next_id(users)
        new_user = User(new_id, username, hashed, salt, role="user")

        users.append(new_user.to_dict())
        self.users_store.save(users)
        return new_user

    def login(self, username, password):
        users = self.users_store.load()
        match = next((u for u in users if u["username"] == username), None)

        if match is None:
            raise ValueError("Invalid username or password.")

        user = User.from_dict(match)
        if not user.check_password(password):
            raise   ValueError("Invalid username or password.")

        with open(self.session_path, "w") as f:
            json.dump({"username": user.username}, f)

        return user

    def logout(self):
        if os.path.exists(self.session_path):
            os.remove(self.session_path)

    def get_current_user(self):
        if not os.path.exists(self.session_path):
            return None

        with open(self.session_path, "r") as f:
            session = json.load(f)

        users = self.users_store.load()
        match = next((u for u in users if u["username"] == session["username"]), None)

        return User.from_dict(match) if match else None