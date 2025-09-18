class DiaryLockedError(Exception):
    """Raised when trying to access diary while it is locked."""
    pass

class DiaryLock:
    """Controls access to te diary(lock/unlock)."""
    def __init__(self, password: str):
        self._password = password
        self._locked = True  # Diary starts locked

    def unlock(self, entered_password: str) -> bool:
        """unlocks the diary if password is correct."""
        if entered_password == self._password:
            self._locked = False #unlocks diary
            return True
        return False

    def lock(self):
        """to lock the diary again e.g if user wants to exit/log out"""
        self._locked = True

    def check_access(self):
        """Raise error if diary is locked"""
        try:
            if self._locked:
                raise DiaryLockedError("🔒 Diary is locked! Please unlock with password.")
        except DiaryLockedError as e:
            print(e)