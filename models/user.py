"""
models/user.py

User - role is a plain string ("user" / "admin").
"""

import hashlib
import os


class User:
    def __init__(self, id, username, password_hash, salt, role="user"):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.role = role

    @staticmethod
    def hash_password(password, salt=None):
        if salt is None:
            salt = os.urandom(16).hex()
        hashed = hashlib.sha256((salt + password).encode()).hexdigest()
        return hashed, salt

    def check_password(self, password):
        hashed, _ = User.hash_password(password, salt=self.salt)
        return hashed == self.password_hash

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            username=d["username"],
            password_hash=d["password_hash"],
            salt=d["salt"],
            role=d.get("role", "user"),
        )