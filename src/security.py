class DiaryLockedError(Exception):
    """Raised when trying to access diary while it is locked or wrong password is used."""
    pass


class DiaryLock:
    """Controls access to the diary (lock/unlock)."""

    def __init__(self, password: str):
        self._password = password
        self._locked = True  # Diary starts locked

    def unlock(self, entered_password: str) -> bool:
        """Unlocks the diary if password is correct, else raises error."""
        if entered_password == self._password:
            self._locked = False  # unlocks diary
            return True
        raise DiaryLockedError("❌ Incorrect password!")

    def lock(self):
        """Locks the diary again e.g., if user wants to exit/log out.
        Raises error if already locked.
        """
        if self._locked:
            raise DiaryLockedError("🔒 Diary is already locked!")
        self._locked = True
        return True

    def check_access(self):
        """Check if diary can be accessed.
        Raises error if diary is locked, otherwise returns access message.
        """
        if self._locked:
            raise DiaryLockedError("🔒 Diary is locked! Please unlock with password.")
        return "📖 Access granted!"
