
import os, json, base64
from datetime import datetime
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

class SecureDiary:
    def __init__(self, password: str, filename="diary.json.enc"):
        self.filename = filename
        self.password = password.encode()
        self.saltfile = "salt.bin"
        self.key = self._derive_key()

    def _derive_key(self):
        if os.path.exists(self.saltfile):
            salt = open(self.saltfile, "rb").read()
        else:
            salt = os.urandom(16)
            open(self.saltfile, "wb").write(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=default_backend()
        )
        return Fernet(base64.urlsafe_b64encode(kdf.derive(self.password)))

    def _load_entries(self):
        if not os.path.exists(self.filename):
            return []
        try:
            encrypted = open(self.filename, "rb").read()
            data = self.key.decrypt(encrypted)
            return json.loads(data.decode())
        except Exception:
            print("❌ Wrong password or corrupted file.")
            return []

    def _save_entries(self, entries):
        data = json.dumps(entries, indent=2).encode()
        encrypted = self.key.encrypt(data)
        open(self.filename, "wb").write(encrypted)

    def add_entry(self, title, content):
        entries = self._load_entries()
        entry_id = len(entries) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entries.append({
            "id": entry_id,
            "title": title,
            "content": content,
            "datetime": timestamp
        })
        self._save_entries(entries)
        print("✅ Entry added securely!")

    def list_entries(self):
        entries = self._load_entries()
        if not entries:
            print("No entries found.")
            return
        for e in entries:
            print(f"[{e['id']}] {e['title']} ({e['datetime']})")
            print(f"   {e['content'][:40]}...\n")

    def update_entry(self, entry_id, new_title=None, new_content=None):
        entries = self._load_entries()
        for e in entries:
            if e["id"] == entry_id:
                if new_title: e["title"] = new_title
                if new_content: e["content"] = new_content
                e["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_entries(entries)
                print("✅ Entry updated!")
                return
        print("❌ Entry not found.")

    def delete_entry(self, entry_id):
        entries = self._load_entries()
        new_entries = [e for e in entries if e["id"] != entry_id]
        if len(new_entries) == len(entries):
            print("❌ Entry not found.")
        else:
            self._save_entries(new_entries)
            print("✅ Entry deleted!")
