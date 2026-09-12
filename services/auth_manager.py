"""
services/auth_manager.py

AuthManager - takes an existing DataStore for users, plus a session_path
where the logged-in user's id is written. The session file is what lets
a login survive between separate `python main.py <command>` runs, since
each invocation is a fresh process with nothing in memory.
"""

import json
import os

from models.user import User


class AuthManager:
    def __init__(self, users_store, session_path):
        self.users_store = users_store
        self.session_path = session_path

    def register(self, username, password, role="user"):
        users = self.users_store.load()
        if any(u["username"] == username for u in users):
            raise ValueError(f"Username '{username}' is already taken.")
        if not password or len(password) < 4:
            raise ValueError("Password must be at least 4 characters.")

        hashed, salt = User.hash_password(password)
        new_id = self.users_store.next_id(users)
        user = User(new_id, username, hashed, salt, role=role)

        users.append(user.to_dict())
        self.users_store.save(users)
        return user

    def login(self, username, password):
        users = self.users_store.load()
        match = next((u for u in users if u["username"] == username), None)
        if match is None:
            raise ValueError("Invalid username or password.")

        user = User.from_dict(match)
        if not user.check_password(password):
            raise ValueError("Invalid username or password.")

        self._save_session(user)
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
        match = next((u for u in users if u["id"] == session["id"]), None)
        if match is None:
            return None
        return User.from_dict(match)

    def _save_session(self, user):
        with open(self.session_path, "w") as f:
            json.dump({"id": user.id, "username": user.username}, f)


# ASSUMPTION — check this against your real main.py: your commands need
# one shared AuthManager so a login in one command is visible to the next
# CLI run. If main.py already builds its own AuthManager, use that one
# instead and delete the two lines below.
from services.data_store import DataStore

default_auth_manager = AuthManager(DataStore("users.json"), session_path="data/session.json")