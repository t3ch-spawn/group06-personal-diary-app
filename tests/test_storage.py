import pytest
import os
import json
from storage import DiaryStorage

TEST_FILE = "test_diary.json"

@pytest.fixture
def storage():
    # make sure no leftover test file
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    return DiaryStorage(filename=TEST_FILE)

def test_add_and_validate_user(storage):
    storage.add_user("user1", "pass123")
    assert storage.validate_user("user1", "pass123") is True
    assert storage.validate_user("user1", "wrong") is False
    assert storage.validate_user("ghost", "pass123") is False

def test_list_entries_empty(storage):
    storage.add_user("user2", "mypass")
    entries = storage.list_entries("user2")
    assert entries == {}

def test_save_and_load(storage):
    storage.add_user("user3", "abc")
    storage.users["user3"]["entries"]["01-01-2025"] = {"title": "New Year", "content": "Start fresh"}
    storage.save_entries()

    # load a new storage object to check persistence
    new_storage = DiaryStorage(filename=TEST_FILE)
    assert "user3" in new_storage.users
    assert "01-01-2025" in new_storage.users["user3"]["entries"]
