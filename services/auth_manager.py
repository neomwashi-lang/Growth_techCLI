"""
services/auth_manager.py

AuthManager and the @login_required / @admin_required decorators.
"""

import functools

from services.data_store import DataStore
from models.user import User, AdminUser, RegularUser


class AuthManager:
    def __init__(self):
        self._store = DataStore("users.json")
        self._session_user = None

    def register(self, username, password, is_admin=False):
        records = self._store.load()
        if any(r["username"] == username for r in records):
            print(f"Username '{username}' is already taken.")
            return None

        cls = AdminUser if is_admin else RegularUser
        user = cls(username=username, password=password)
        user.id = DataStore.next_id(records)
        records.append(user.to_dict())
        self._store.save(records)
        print(f"Registered {'admin' if is_admin else 'user'} '{username}'.")
        return user

    def login(self, username, password):
        records = self._store.load()
        match = next((r for r in records if r["username"] == username), None)
        if match is None:
            print("No such user.")
            return None

        user = User.from_dict(match)
        if not user.check_password(password):
            print("Incorrect password.")
            return None

        self._session_user = user
        print(f"Logged in as '{username}'.")
        return user

    def logout(self):
        self._session_user = None

    def current_user(self):
        return self._session_user


auth_manager = AuthManager()


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if auth_manager.current_user() is None:
            print("You must be logged in to do that.")
            return None
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = auth_manager.current_user()
        if user is None or not user.is_admin:
            print("Admin access required.")
            return None
        return func(*args, **kwargs)
    return wrapper