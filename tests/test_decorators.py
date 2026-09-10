
from models.user import User
from services.data_store import DataStore
from services.auth_manager import AuthManager
from utils.decorators import login_required, admin_required

def make_auth(tmp_path):
    users_store = DataStore(tmp_path / "users.json")
    session_path = tmp_path / "session.json"
    return AuthManager(users_store, session_path=session_path)

def test_login_required_blocks_logged_out_user(tmp_path):
    auth = make_auth(tmp_path)

    @login_required(auth)
    def fake_command():
        return "ran"

    result = fake_command()
    assert result is None

def test_login_required_allows_logged_in_user(tmp_path):
    auth = make_auth(tmp_path)
    auth.register("neo", "hunter2")
    auth.login("neo", "hunter2")

    @login_required(auth)
    def fake_command():
        return "ran"

    result = fake_command()
    assert result == "ran"

def test_admin_required_blocks_regular_user(tmp_path):
    auth = make_auth(tmp_path)
    auth.register("neo", "hunter2")   # role defaults to "user"
    auth.login("neo", "hunter2")

    @admin_required(auth)
    def fake_admin_command():
        return "ran"

    result = fake_admin_command()
    assert result is None

def test_admin_required_allows_admin(tmp_path):
    users_store = DataStore(tmp_path / "users.json")
    session_path = tmp_path / "session.json"
    auth = AuthManager(users_store, session_path=session_path)

    # AuthManager.register() can't create admins yet — this is the
    # gap flagged above. Bypassing it here to build one directly.
    hashed, salt = User.hash_password("adminpass")
    admin_user = User(1, "boss", hashed, salt, role="admin")
    users_store.save([admin_user.to_dict()])

    auth.login("boss", "adminpass")

    @admin_required(auth)
    def fake_admin_command():
        return "ran"

    result = fake_admin_command()
    assert result == "ran"