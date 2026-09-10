"""
services/transaction_service.py

Story 3: Add Transaction.
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
