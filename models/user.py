
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

        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            100_00
        ).hex()

        return hashed, salt

    def check_password(self, password):
        hashed, _ =User.hash_password(password, salt=self.salt)
        return hashed == self.password_hash

    def to_dict(self):
       return {
           "id": self.id,
           "username": self.username,
           "password_hash": self.password_hash,
           "salt": self.salt,
           "role": self.role,
       }

    @staticmethod
    def from_dict(data):
       return User(
           id=data["id"],
           username=data["username"],
           password_hash=data["password_hash"],
           salt=data["salt"],
           role=data["role"]
       )