
import json
import os

class DataStore:
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save(self, records):
        # ensure the parent folder (e.g. "data/") exists before writing
        folder = os.path.dirname(self.filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        with open(self.filepath, "w") as f:
            json.dump(records, f, indent=2)

    def next_id(self, records):
        if not records:
            return 1
        return max(record["id"] for record in records) + 1