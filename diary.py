entries = {
  "entries": [
    {
      "id": 1,
      "date": "12-08-2025",
      "time": "09:15",
      "title": "Morning Coding Session",
      "content": "Had a productive morning coding the diary project."
    },
    {
      "id": 2,
      "date": "16-09-2025",
      "time": "20:10",
      "title": "Evening Tennis",
      "content": "Played tennis in the evening, felt great!"
    },
    {
      "id": 3,
      "date": "03-07-2025",
      "time": "14:45",
      "title": "Library Research",
      "content": "Went to the library to research project ideas."
    },
    {
      "id": 4,
      "date": "01-09-2025",
      "time": "18:30",
      "title": "Movie Night",
      "content": "Watched a movie with friends after class."
    },
    {
      "id": 5,
      "date": "25-06-2025",
      "time": "11:00",
      "title": "Gym Workout",
      "content": "Worked out at the gym, feeling stronger."
    },
    {
      "id": 6,
      "date": "05-08-2025",
      "time": "21:20",
      "title": "Team Call",
      "content": "Had a long call with my project teammates."
    },
    {
      "id": 7,
      "date": "10-09-2025",
      "time": "08:05",
      "title": "Morning Walk",
      "content": "Early morning walk to clear my head."
    },
    {
      "id": 8,
      "date": "22-07-2025",
      "time": "16:40",
      "title": "Debugging Session",
      "content": "Spent the afternoon debugging Python code."
    },
    {
      "id": 9,
      "date": "22-07-2025",
      "time": "13:25",
      "title": "Family Lunch",
      "content": "Visited family and had lunch together."
    },
    {
      "id": 10,
      "date": "14-09-2025",
      "time": "19:55",
      "title": "Presentation Prep",
      "content": "Prepared slides for tomorrow’s presentation."
    }
  ]
}

class No_Result_Error(Exception):
    def __init__(self, result_type=None, content=None):
        self.message = f"There are no search results for {result_type}: {content}"
        super().__init__(self.message)


class Diary:
    def __init__(self):
        pass

    def search_by_date(self, date):
        try:
            results = []
            for entry in entries["entries"]:
                if entry["date"] == date:
                    results.append(entry)

            if len(results) == 0:
                raise No_Result_Error("date", date)
            return results
        except No_Result_Error as e:
            print(e)

    def edit_entry(self, entry_id, new_title=None, new_content=None):
        try:
            for entry in entries["entries"]:
                if entry["id"] == entry_id:
                    if new_title:
                        entry["title"] = new_title
                    if new_content:
                        entry["content"] = new_content
                    print("✅ Entry updated successfully.")
                    return entry

            raise No_Result_Error("id", entry_id)
        except No_Result_Error as e:
            print(e)

    def delete_entry(self, entry_id):
        try:
            for entry in entries["entries"]:
                if entry["id"] == entry_id:
                    entries["entries"].remove(entry)
                    print("🗑️ Entry deleted successfully.")
                    return
            raise No_Result_Error("id", entry_id)
        except No_Result_Error as e:
            print(e)



