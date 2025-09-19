# storage.py
import json
import os
from datetime import datetime

class DiaryStorage:
    def __init__(self, filename="diary.json"):
        self.filename = filename
        self.entries = []
        self.load_entries()

    # Saves entries to JSON file
    def save_entries(self, entries):
        with open(self.filename, "w") as f:
            json.dump(entries, f, indent=4)

    # Load entries from JSON file
    def load_entries(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.entries = json.load(f)
        else:
            self.entries = []

    # Listing entries: It returns an array of the entries in the json file
    def list_entries(self):
        if not self.entries:
            return []
        else:
            return self.entries
