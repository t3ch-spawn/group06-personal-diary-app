# storage.py
import json
import os
from datetime import datetime

class DiaryStorage:
    def __init__(self, filename="diary.json"):
        self.filename = filename
        self.data = {"entries": []}
        self.load_entries()

    # Save entries to JSON file
    def save_entries(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    # Load entries from JSON file
    def load_entries(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"entries": []}

    # Add new entry
    def add_entry(self, title, content):
        entry_id = len(self.data["entries"]) + 1
        now = datetime.now()
        entry = {
            "id": entry_id,
            "title": title,
            "content": content,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S")
        }
        self.data["entries"].append(entry)
        self.save_entries()

    # View all entries
    def view_entries(self):
        return self.data["entries"]

    # listing entries 
    def list_entries(self):
        if not self.data["entries"]:
            print("No entries yet.")
        else:
            for e in self.data["entries"]:
                print(f"{e['id']}. {e['title']} - {e['date']} {e['time']}")
                print(f"   {e['content']}")
