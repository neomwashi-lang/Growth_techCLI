"""
services/transaction_service.py

Story 3: Add Transaction.
Story 4: List Transactions.
"""

from services.data_store import DataStore
from services.auth_manager import login_required, auth_manager
from models.transaction import Transaction

_store = DataStore("transactions.json")


@login_required
def add_transaction(amount, category, date, description=""):
    """Story 3: Add Transaction."""
    user = auth_manager.current_user()
    records = _store.load()

    txn = Transaction(
        id=DataStore.next_id(records),
        user=user.username,
        amount=amount,
        category=category,
        date=date,
        description=description,
    )
    records.append(txn.to_dict())
    _store.save(records)
    print(f"Added transaction #{txn.id}: {category} {amount} on {date}")
    return txn


@login_required
def list_transactions():
    """Story 4: List Transactions (only the current user's own)."""
    user = auth_manager.current_user()
    records = _store.load()
    mine = [r for r in records if r["user"] == user.username]

    if not mine:
        print("No transactions yet.")
        return []

    for r in mine:
        print(f"#{r['id']}  {r['date']}  {r['category']:<15} {r['amount']:>10}  {r['description']}")
    return [Transaction.from_dict(r) for r in mine]