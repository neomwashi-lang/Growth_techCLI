"""
models/budget.py

Budget: one spending limit per (user, category, month).
"""


class Budget:
    def __init__(self, user, category, month, limit, id=None):
        self.id = id
        self.user = user
        self.category = category
        self.month = month
        self.limit = limit

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "category": self.category,
            "month": self.month,
            "limit": self.limit,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            user=d["user"],
            category=d["category"],
            month=d["month"],
            limit=d["limit"],
        )

    def __repr__(self):
        return f"<Budget #{self.id} {self.user} {self.category} {self.month} limit={self.limit}>"