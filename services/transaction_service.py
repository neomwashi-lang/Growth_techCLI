"""
services/transaction_service.py

Story 3: Add Transaction.
Story 4: List Transactions.
Story 5: Show Transaction.
Story 6: Edit/Delete Transaction.
"""

from services.data_store import DataStore
from services.auth_manager import default_auth_manager
from utils.decorators import login_required
from models.transaction import Transaction

_store = DataStore("transactions.json")


@login_required(default_auth_manager)
def add_transaction(amount, category, date, description=""):
    """Story 3: Add Transaction."""
    user = default_auth_manager.get_current_user()
    records = _store.load()

    txn = Transaction(
        id=_store.next_id(records),
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


@login_required(default_auth_manager)
def list_transactions():
    """Story 4: List Transactions (only the current user's own)."""
    user = default_auth_manager.get_current_user()
    records = _store.load()
    mine = [r for r in records if r["user"] == user.username]

    if not mine:
        print("No transactions yet.")
        return []

    for r in mine:
        print(f"#{r['id']}  {r['date']}  {r['category']:<15} {r['amount']:>10}  {r['description']}")
    return [Transaction.from_dict(r) for r in mine]


@login_required(default_auth_manager)
def show_transaction(txn_id):
    """Story 5: Show a single Transaction (must belong to current user)."""
    user = default_auth_manager.get_current_user()
    records = _store.load()
    match = next((r for r in records if r["id"] == txn_id), None)

    if match is None:
        print(f"No transaction with id {txn_id}.")
        return None
    if match["user"] != user.username:
        print("That transaction doesn't belong to you.")
        return None

    txn = Transaction.from_dict(match)
    print(txn)
    return txn


@login_required(default_auth_manager)
def edit_transaction(txn_id, amount=None, category=None, date=None, description=None):
    """Story 6 (part 1): Edit a Transaction you own."""
    user = default_auth_manager.get_current_user()
    records = _store.load()
    match = next((r for r in records if r["id"] == txn_id), None)

    if match is None:
        print(f"No transaction with id {txn_id}.")
        return None
    if match["user"] != user.username:
        print("That transaction doesn't belong to you.")
        return None

    if amount is not None:
        match["amount"] = amount
    if category is not None:
        match["category"] = category
    if date is not None:
        match["date"] = date
    if description is not None:
        match["description"] = description

    _store.save(records)
    print(f"Updated transaction #{txn_id}.")
    return Transaction.from_dict(match)


@login_required(default_auth_manager)
def delete_transaction(txn_id):
    """Story 6 (part 2): Delete a Transaction you own."""
    user = default_auth_manager.get_current_user()
    records = _store.load()
    match = next((r for r in records if r["id"] == txn_id), None)

    if match is None:
        print(f"No transaction with id {txn_id}.")
        return False
    if match["user"] != user.username:
        print("That transaction doesn't belong to you.")
        return False

    records = [r for r in records if r["id"] != txn_id]
    _store.save(records)
    print(f"Deleted transaction #{txn_id}.")
    return True