import pytest

import services.auth_manager as auth_module
import services.budget_service as budget_module
from services.data_store import DataStore
from services.budget_service import set_budget, list_budgets, current_month


@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    auth = auth_module.default_auth_manager
    monkeypatch.setattr(auth, "users_store", DataStore(tmp_path / "users.json"))
    monkeypatch.setattr(auth, "session_path", tmp_path / "session.json")
    monkeypatch.setattr(budget_module, "_store", DataStore(tmp_path / "budgets.json"))

    auth.register("testuser", "password123")
    auth.login("testuser", "password123")
    yield


def test_set_budget_creates_record():
    b = set_budget("Groceries", 200)
    assert b.category == "Groceries"
    assert b.limit == 200
    assert b.month == current_month()


def test_set_budget_updates_existing_rather_than_duplicating():
    b1 = set_budget("Groceries", 200)
    b2 = set_budget("Groceries", 250)
    assert b2.id == b1.id
    records = budget_module._store.load()
    assert len(records) == 1
    assert records[0]["limit"] == 250


def test_set_budget_requires_login():
    auth_module.default_auth_manager.logout()
    assert set_budget("Groceries", 200) is None


def test_list_budgets_returns_only_current_user():
    set_budget("Groceries", 200)
    budget_module._store.save(budget_module._store.load() + [{
        "id": 999, "user": "someone_else", "category": "Rent",
        "month": current_month(), "limit": 500,
    }])

    results = list_budgets()
    assert len(results) == 1
    assert results[0].user == "testuser"


def test_list_budgets_empty():
    assert list_budgets() == []