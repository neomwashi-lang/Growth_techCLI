import pytest

import services.auth_manager as auth_module
import services.transaction_service as txn_module
import services.budget_service as budget_module
import services.report_service as report_module
from services.data_store import DataStore
from services.transaction_service import add_transaction
from services.budget_service import set_budget, current_month
from services.report_service import generate_report


@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    auth = auth_module.default_auth_manager
    monkeypatch.setattr(auth, "users_store", DataStore(tmp_path / "users.json"))
    monkeypatch.setattr(auth, "session_path", tmp_path / "session.json")
    monkeypatch.setattr(txn_module, "_store", DataStore(tmp_path / "transactions.json"))
    monkeypatch.setattr(budget_module, "_store", DataStore(tmp_path / "budgets.json"))
    monkeypatch.setattr(report_module, "_txn_store", DataStore(tmp_path / "transactions.json"))
    monkeypatch.setattr(report_module, "_budget_store", DataStore(tmp_path / "budgets.json"))

    auth.register("testuser", "password123")
    auth.login("testuser", "password123")
    yield


def test_report_totals_income_and_expenses():
    month = current_month()
    add_transaction(amount=1000, category="Salary", date=f"{month}-01")
    add_transaction(amount=-200, category="Groceries", date=f"{month}-02")

    result = generate_report()
    assert result["income"] == 1000
    assert result["expenses"] == -200


def test_report_flags_over_budget_category():
    month = current_month()
    set_budget("Groceries", 100)
    add_transaction(amount=-150, category="Groceries", date=f"{month}-05")

    result = generate_report()
    assert "Groceries" in result["over_budget"]


def test_report_does_not_flag_under_budget_category():
    month = current_month()
    set_budget("Groceries", 200)
    add_transaction(amount=-50, category="Groceries", date=f"{month}-05")

    result = generate_report()
    assert "Groceries" not in result["over_budget"]


def test_report_ignores_other_months():
    add_transaction(amount=-50, category="Groceries", date="2020-01-15")
    result = generate_report()
    assert result["by_category"] == {}


def test_report_requires_login():
    auth_module.default_auth_manager.logout()
    assert generate_report() is None