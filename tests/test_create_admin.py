
from services.data_store import DataStore
from scripts.create_admin import create_admin

def test_create_admin_sets_role_admin(tmp_path):
    store = DataStore(tmp_path / "users.json")
    admin = create_admin("boss", "adminpass", store)
    assert admin.role == "admin"

def test_create_admin_duplicate_username_raises(tmp_path):
    store = DataStore(tmp_path / "users.json")
    create_admin("boss", "adminpass", store)
    try:
        create_admin("boss", "different", store)
        assert False, "expected ValueError for duplicate username"
    except ValueError:
        pass