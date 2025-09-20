import pytest
from diary import Diary

class FakeStorage:
    """Fake storage so we don’t use real files"""
    def __init__(self):
        self.users = {"user1": {"entries": {}}}

    def load_users(self):
        return self.users

    def list_entries(self, username):
        return self.users[username]["entries"]

    def save_entries(self, users_list):
        self.users = users_list


@pytest.fixture
def diary():
    diary = Diary()
    diary.store = FakeStorage()
    diary.users_list = diary.store.load_users()
    return diary


def test_create_entry(diary):
    entry = {"title": "Test", "content": "Content", "date": "01-01-2025"}
    diary.create_entry(entry, "user1")
    assert "01-01-2025" in diary.store.list_entries("user1")


def test_delete_entry(diary):
    entry = {"title": "DeleteMe", "content": "Bye", "date": "02-01-2025"}
    diary.create_entry(entry, "user1")
    assert diary.delete_entry("02-01-2025", "user1") is True


def test_search_by_keyword(diary):
    entry = {"title": "Morning", "content": "Routine", "date": "03-01-2025"}
    diary.create_entry(entry, "user1")
    results = diary.search_by_keyword("Morning", "user1")
    assert len(results) == 1


def test_search_by_date(diary):
    entry = {"title": "Meeting", "content": "At 10 AM", "date": "04-01-2025"}
    diary.create_entry(entry, "user1")
    results = diary.search_by_date("04-01-2025", "user1")
    assert len(results) == 1