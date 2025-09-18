class Diary:
    def __init__(self):
        self.id = 1
        self.date = "2025-09-16"
        self.time = "14:30"
        self.content = "Today I worked on the group project setup."
        self.user = "user1"

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "time": self.time,
            "content": self.content,
            "user": self.user
        }

# Example usage
entry = LogEntry()
print(entry.to_dict())
