"""
services/data_store.py

DataStore - no database, one JSON file per entity under data/, and only
DataStore is allowed to touch those files directly.
"""

import json
import os


class DataStore:
    def __init__(self, filename):
        os.makedirs("data", exist_ok=True)
        self.filename = os.path.join("data", filename)
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def save(self, records):
        with open(self.filename, "w") as f:
            json.dump(records, f, indent=2)

    @staticmethod
    def next_id(records):
        if not records:
            return 1
        return max(r["id"] for r in records) + 1
