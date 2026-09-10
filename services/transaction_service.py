"""
services/transaction_service.py

Story 3: Add Transaction.
Story 4: List Transactions.
Story 5: Show Transaction.
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
