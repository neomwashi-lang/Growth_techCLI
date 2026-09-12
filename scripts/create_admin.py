import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.data_store import DataStore
from models.user import User

def create_admin(username, password, users_store):   
    users = users_store.load()

    if any(u["username"] == username for u in users):
        raise ValueError(f"Username '{username}' is already taken.")
    if not password or len(password) < 4:
        raise ValueError("Password must be at least 4 characters.")

    hashed, salt = User.hash_password(password)
    new_id = users_store.next_id(users)
    admin_user = User(new_id, username, hashed, salt, role="admin")

    users.append(admin_user.to_dict())
    users_store.save(users)
    return admin_user
if __name__ == "__main__":
    store = DataStore("data/users.json")
    username = input("Admin username: ")
    password = input("Admin password: ")

    try:
        create_admin(username, password, store)
        print(f"Admin '{username}' created successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        