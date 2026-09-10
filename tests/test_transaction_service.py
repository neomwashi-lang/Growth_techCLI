"""
tests/test_transaction_service.py
"""

import pytest

import services.auth_manager as auth_module
import services.transaction_service as txn_module
from services.transaction_service import add_transaction, list_transactions


@pytest.fixture(autouse=True)
def clean_state():
    txn_module._store.save([])
    auth_module.auth_manager._store.save([])
    auth_module.auth_manager.logout()
    auth_module.auth_manager.register("testuser", "password123")
    auth_module.auth_manager.login("testuser", "password123")
    yield
    txn_module._store.save([])
    auth_module.auth_manager._store.save([])
    auth_module.auth_manager.logout()


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
    auth_module.auth_manager.logout()
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
    auth_module.auth_manager.logout()
    assert list_transactions() is None