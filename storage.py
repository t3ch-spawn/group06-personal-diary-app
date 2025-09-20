# storage.py
import json
import os
from datetime import datetime

class DiaryStorage:
    def __init__(self, filename="diary.json"):
        self.filename = filename
        self.users = {}  # Holds users and their diary data
        self.load_users()

    # Saves all users' data to JSON file
    def save_entries(self, users=None):
        if users is not None:
            self.users = users
        with open(self.filename, "w") as f:
            json.dump(self.users, f, indent=4)

    # Load users and their entries from JSON file
    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.users = json.load(f)
                return self.users
        else:
            self.users = {}
            return self.users

    # Listing entries for a specific user
    def list_entries(self, username):
        if username in self.users:
            return self.users[username].get("entries", {})
        return {}

    # Add a new user
    def add_user(self, username, password):
        if username not in self.users:
            self.users[username] = {
                "password": password,
                "entries": {}
            }
            self.save_entries()

    # Validate user login
    def validate_user(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            return True
        return False
