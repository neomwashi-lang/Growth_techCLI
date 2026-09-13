"""
tests/test_transaction_service.py
"""

import pytest

import services.auth_manager as auth_module
import services.transaction_service as txn_module
from services.data_store import DataStore
from services.transaction_service import add_transaction, list_transactions, show_transaction, edit_transaction, delete_transaction


@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    auth = auth_module.default_auth_manager
    monkeypatch.setattr(auth, "users_store", DataStore(tmp_path / "users.json"))
    monkeypatch.setattr(auth, "session_path", tmp_path / "session.json")
    monkeypatch.setattr(txn_module, "_store", DataStore(tmp_path / "transactions.json"))

    auth.register("testuser", "password123")
    auth.login("testuser", "password123")
    yield


def test_add_transaction_creates_record():
    t = add_transaction(amount=-45.50, category="Groceries", date="2026-09-01", description="Weekly shop")
    assert t.id == 1
    assert t.user == "testuser"
    assert t.amount == -45.50
    assert t.category == "Groceries"

    records = txn_module._store.load()
    assert len(records) == 1
    assert records[0]["description"] == "Weekly shop"


def test_add_transaction_ids_increment():
    t1 = add_transaction(amount=-10, category="Food", date="2026-09-01")
    t2 = add_transaction(amount=-20, category="Food", date="2026-09-02")
    assert t2.id == t1.id + 1


def test_add_transaction_requires_login():
    auth_module.default_auth_manager.logout()
    result = add_transaction(amount=-10, category="Food", date="2026-09-01")
    assert result is None
    assert txn_module._store.load() == []


# --- Story 4: List Transactions ---

def test_list_transactions_returns_only_current_user():
    add_transaction(amount=-10, category="Food", date="2026-09-01")

    # a transaction belonging to someone else shouldn't show up
    txn_module._store.save(txn_module._store.load() + [{
        "id": 999, "user": "someone_else", "amount": -5,
        "category": "Food", "date": "2026-09-01", "description": "not mine",
    }])

    results = list_transactions()
    assert len(results) == 1
    assert results[0].user == "testuser"


def test_list_transactions_empty():
    results = list_transactions()
    assert results == []


def test_list_transactions_requires_login():
    auth_module.default_auth_manager.logout()
    assert list_transactions() is None


# --- Story 5: Show Transaction ---

def test_show_transaction_returns_correct_one():
    t1 = add_transaction(amount=-10, category="Food", date="2026-09-01")
    add_transaction(amount=-20, category="Rent", date="2026-09-02")

    shown = show_transaction(t1.id)
    assert shown.id == t1.id
    assert shown.category == "Food"


def test_show_transaction_nonexistent_returns_none():
    assert show_transaction(9999) is None


def test_show_transaction_wrong_owner_returns_none():
    t1 = add_transaction(amount=-10, category="Food", date="2026-09-01")

    # add a second user and try to view the first user's transaction
    auth = auth_module.default_auth_manager
    auth.register("otheruser", "password123")
    auth.login("otheruser", "password123")

    assert show_transaction(t1.id) is None


def test_show_transaction_requires_login():
    auth_module.default_auth_manager.logout()
    assert show_transaction(1) is None


# --- Story 6: Edit / Delete Transaction ---

def test_edit_transaction_updates_fields():
    t1 = add_transaction(amount=-10, category="Food", date="2026-09-01", description="old")
    updated = edit_transaction(t1.id, amount=-15, description="new")

    assert updated.amount == -15
    assert updated.description == "new"
    assert updated.category == "Food"  # untouched fields stay the same


def test_edit_transaction_nonexistent_returns_none():
    assert edit_transaction(9999, amount=-1) is None


def test_edit_transaction_wrong_owner_returns_none_and_does_not_change():
    t1 = add_transaction(amount=-10, category="Food", date="2026-09-01")

    auth = auth_module.default_auth_manager
    auth.register("otheruser", "password123")
    auth.login("otheruser", "password123")

    result = edit_transaction(t1.id, amount=-999)
    assert result is None

    auth.login("testuser", "password123")
    unchanged = show_transaction(t1.id)
    assert unchanged.amount == -10


def test_edit_transaction_requires_login():
    auth_module.default_auth_manager.logout()
    assert edit_transaction(1, amount=-1) is None


def test_delete_transaction_removes_record():
    t1 = add_transaction(amount=-10, category="Food", date="2026-09-01")
    assert delete_transaction(t1.id) is True
    assert show_transaction(t1.id) is None
    assert list_transactions() == []


def test_delete_transaction_nonexistent_returns_false():
    assert delete_transaction(9999) is False


def test_delete_transaction_wrong_owner_returns_false_and_does_not_delete():
    t1 = add_transaction(amount=-10, category="Food", date="2026-09-01")

    auth = auth_module.default_auth_manager
    auth.register("otheruser2", "password123")
    auth.login("otheruser2", "password123")

    assert delete_transaction(t1.id) is False

    auth.login("testuser", "password123")
    assert show_transaction(t1.id) is not None


def test_delete_transaction_requires_login():
    auth_module.default_auth_manager.logout()
    assert delete_transaction(1) is None