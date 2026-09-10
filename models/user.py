"""
models/user.py

User, AdminUser, RegularUser - shared account fields live once in the
base class, role-specific behavior is added on top.
"""

import hashlib
import os


class User:
    def __init__(self, username, password_hash=None, salt=None, password=None, id=None):
        self.id = id
        self.username = username

        if password is not None:
            self.salt = os.urandom(16).hex()
            self.password_hash = self._hash_password(password, self.salt)
        else:
            self.password_hash = password_hash
            self.salt = salt

    @staticmethod
    def _hash_password(password, salt):
        return hashlib.sha256((salt + password).encode()).hexdigest()

    def check_password(self, password):
        return self._hash_password(password, self.salt) == self.password_hash

    @property
    def is_admin(self):
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "role": "admin" if self.is_admin else "regular",
        }

    @classmethod
    def from_dict(cls, d):
        role = d.get("role", "regular")
        target_cls = AdminUser if role == "admin" else RegularUser
        return target_cls(username=d["username"], password_hash=d["password_hash"], salt=d["salt"], id=d["id"])


class RegularUser(User):
    pass


class AdminUser(User):
    @property
    def is_admin(self):
        return True
