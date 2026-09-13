"""
services/budget_service.py

Story 7: Set a Monthly Budget.

One budget per (user, category, month) — setting it again updates the
existing record rather than creating a duplicate, per the acceptance
criteria. Rather than encoding that triple as a single JSON key, budgets
are stored as a flat list and matched by filtering on all three fields.
"""

from datetime import date

from services.data_store import DataStore
from services.auth_manager import default_auth_manager
from utils.decorators import login_required
from models.budget import Budget

_store = DataStore("budgets.json")


def current_month():
    return date.today().strftime("%Y-%m")


@login_required(default_auth_manager)
def set_budget(category, limit, month=None):
    """Create or update the budget for (current user, category, month)."""
    user = default_auth_manager.get_current_user()
    month = month or current_month()
    records = _store.load()

    match = next(
        (r for r in records if r["user"] == user.username
         and r["category"] == category and r["month"] == month),
        None,
    )

    if match is not None:
        match["limit"] = limit
        _store.save(records)
        print(f"Updated budget for {category} ({month}) to {limit}.")
        return Budget.from_dict(match)

    budget = Budget(
        id=_store.next_id(records),
        user=user.username,
        category=category,
        month=month,
        limit=limit,
    )
    records.append(budget.to_dict())
    _store.save(records)
    print(f"Set budget for {category} ({month}) to {limit}.")
    return budget


@login_required(default_auth_manager)
def list_budgets():
    """List the current user's budgets."""
    user = default_auth_manager.get_current_user()
    records = _store.load()
    mine = [r for r in records if r["user"] == user.username]

    if not mine:
        print("No budgets set yet.")
        return []

    for r in mine:
        print(f"{r['category']:<15} {r['month']}  limit={r['limit']}")
    return [Budget.from_dict(r) for r in mine]