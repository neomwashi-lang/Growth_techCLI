"""
models/transaction.py

Transaction and Category.
"""


class Transaction:
    def __init__(self, user, amount, category, date, description="", id=None):
        self.id = id
        self.user = user
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            user=d["user"],
            amount=d["amount"],
            category=d["category"],
            date=d["date"],
            description=d.get("description", ""),
        )

    def __repr__(self):
        return f"<Transaction #{self.id} {self.date} {self.category} {self.amount}>"


class Category:
    def __init__(self, user, name, id=None):
        self.id = id
        self.user = user
        self.name = name

    def to_dict(self):
        return {"id": self.id, "user": self.user, "name": self.name}

    @classmethod
    def from_dict(cls, d):
        return cls(id=d["id"], user=d["user"], name=d["name"])

    def __repr__(self):
        return f"<Category #{self.id} {self.name}>"