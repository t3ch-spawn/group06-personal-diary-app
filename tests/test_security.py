import pytest
from src.security import DiaryLock, DiaryLockedError


def test_unlock_with_wrong_password():
    """Unlocking with the wrong password should raise DiaryLockedError"""
    lock = DiaryLock("mypassword")
    with pytest.raises(DiaryLockedError):
        lock.unlock("wrong")


def test_lock_and_unlock_cycle():
    """Test locking and unlocking multiple times"""
    lock = DiaryLock("mypassword")
    # Unlock should work with the right password
    assert lock.unlock("mypassword") is True
    # Lock again
    lock.lock()
    # Should raise error if trying to lock again while already locked
    with pytest.raises(DiaryLockedError):
        lock.lock()


def test_check_access_while_locked():
    """Access should raise DiaryLockedError if diary is locked"""
    lock = DiaryLock("mypassword")
    with pytest.raises(DiaryLockedError):
        lock.check_access()
