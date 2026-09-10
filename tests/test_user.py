from models.user import User

def test_hash_password_returns_hash_and_salt():
    hashed, salt = User.hash_password("hunter2")
    assert hashed is not None
    assert salt is not None

def test_check_password_correct():
    hashed, salt = User.hash_password("hunter2")
    u = User(1, "neo", hashed, salt, role="user")
    assert u.check_password("hunter2") is True

def test_check_password_wrong():
    hashed, salt = User.hash_password("hunter2")
    u = User(1, "neo", hashed, salt, role="user")
    assert u.check_password("wrong") is False

def test_to_dict_and_from_dict_roundtrip():
    hashed, salt = User.hash_password("hunter2")
    u = User(1, "neo", hashed, salt, role="admin")
    rebuilt = User.from_dict(u.to_dict())
    assert rebuilt.username == u.username
    assert rebuilt.role == u.role
    assert rebuilt.check_password("hunter2") is True