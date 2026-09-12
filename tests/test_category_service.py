"""
tests/test_category_service.py
"""

import pytest

import services.auth_manager as auth_module
import services.category_service as cat_module
from services.category_service import add_category, list_categories, edit_category, delete_category


@pytest.fixture(autouse=True)
def clean_state():
    cat_module._store.save([])
    auth = auth_module.default_auth_manager
    auth.users_store.save([])
    auth.logout()
    auth.register("testadmin", "password123", role="admin")
    auth.login("testadmin", "password123")
    yield
    cat_module._store.save([])
    auth.users_store.save([])
    auth.logout()


def test_add_category_creates_record():
    c = add_category("Groceries")
    assert c.id == 1
    assert c.name == "Groceries"
    assert c.user == "testadmin"

    records = cat_module._store.load()
    assert len(records) == 1


def test_add_category_ids_increment():
    c1 = add_category("Groceries")
    c2 = add_category("Rent")
    assert c2.id == c1.id + 1


def test_add_category_requires_admin():
    auth_module.default_auth_manager.logout()
    auth_module.default_auth_manager.register("regularuser", "password123")  # role defaults to "user"
    auth_module.default_auth_manager.login("regularuser", "password123")

    result = add_category("Groceries")
    assert result is None
    assert cat_module._store.load() == []


def test_add_category_requires_login():
    auth_module.default_auth_manager.logout()
    assert add_category("Groceries") is None


def test_list_categories_returns_all():
    add_category("Groceries")
    add_category("Rent")
    results = list_categories()
    assert len(results) == 2
    assert {c.name for c in results} == {"Groceries", "Rent"}


def test_list_categories_empty():
    assert list_categories() == []


def test_edit_category_updates_name():
    c = add_category("Groceries")
    updated = edit_category(c.id, "Food & Groceries")
    assert updated.name == "Food & Groceries"


def test_edit_category_nonexistent_returns_none():
    assert edit_category(9999, "Whatever") is None


def test_edit_category_requires_admin():
    c = add_category("Groceries")

    auth_module.default_auth_manager.logout()
    auth_module.default_auth_manager.register("regularuser", "password123")
    auth_module.default_auth_manager.login("regularuser", "password123")

    result = edit_category(c.id, "Hacked name")
    assert result is None

    auth_module.default_auth_manager.login("testadmin", "password123")
    records = cat_module._store.load()
    assert records[0]["name"] == "Groceries"  # unchanged


def test_delete_category_removes_record():
    c = add_category("Groceries")
    assert delete_category(c.id) is True
    assert cat_module._store.load() == []


def test_delete_category_nonexistent_returns_false():
    assert delete_category(9999) is False


def test_delete_category_requires_admin():
    c = add_category("Groceries")

    auth_module.default_auth_manager.logout()
    auth_module.default_auth_manager.register("regularuser", "password123")
    auth_module.default_auth_manager.login("regularuser", "password123")

    assert delete_category(c.id) is None

    auth_module.default_auth_manager.login("testadmin", "password123")
    assert len(cat_module._store.load()) == 1  # still there