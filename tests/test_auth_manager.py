
from services.data_store import DataStore
from services.auth_manager import AuthManager

def make_auth(tmp_path):
    users_store = DataStore(tmp_path / "users.json")
    session_path = tmp_path / "session.json"
    return AuthManager(users_store, session_path=session_path)

def test_register_creates_user(tmp_path):
    auth = make_auth(tmp_path)
    user = auth.register("neo", "hunter2")
    assert user.username == "neo"
    assert user.role == "user"

def test_register_duplicate_username_raises(tmp_path):
    auth = make_auth(tmp_path)
    auth.register("neo", "hunter2")
    try:
        auth.register("neo", "different")
        assert False, "expected ValueError for duplicate username"
    except ValueError:
        pass

def test_register_weak_password_raises(tmp_path):
    auth = make_auth(tmp_path)
    try:
        auth.register("neo", "abc")
        assert False, "expected ValueError for weak password"
    except ValueError:
        pass

def test_login_success(tmp_path):
    auth = make_auth(tmp_path)
    auth.register("neo", "hunter2")
    user = auth.login("neo", "hunter2")
    assert user.username == "neo"

def test_login_wrong_password_raises(tmp_path):
    auth = make_auth(tmp_path)
    auth.register("neo", "hunter2")
    try:
        auth.login("neo", "wrongpass")
        assert False, "expected ValueError for wrong password"
    except ValueError:
        pass

def test_login_unknown_user_raises(tmp_path):
    auth = make_auth(tmp_path)
    try:
        auth.login("ghost", "whatever")
        assert False, "expected ValueError for unknown username"
    except ValueError:
        pass

def test_get_current_user_after_login(tmp_path):
    auth = make_auth(tmp_path)
    auth.register("neo", "hunter2")
    auth.login("neo", "hunter2")
    current = auth.get_current_user()
    assert current is not None
    assert current.username == "neo"

def test_get_current_user_returns_none_when_logged_out(tmp_path):
    auth = make_auth(tmp_path)
    assert auth.get_current_user() is None

def test_logout_clears_session(tmp_path):
    auth = make_auth(tmp_path)
    auth.register("neo", "hunter2")
    auth.login("neo", "hunter2")
    auth.logout()
    assert auth.get_current_user() is None