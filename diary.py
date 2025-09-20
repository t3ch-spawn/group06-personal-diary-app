# diary.py
from datetime import datetime
from storage import DiaryStorage
import re

class Diary:
    def __init__(self):
        self.store = DiaryStorage()
        self.entries_list = self.store.list_entries()

# This function creates and edits entries using the date assigned to the entry as a key
    def create_entry(self, entry):
        """Add a new entry keyed by date (dd-mm-yyyy)"""
        date_key = entry["date"]
        

        # Assign ID based on number of existing entries
        entry["id"] = len(self.entries_list) + 1
        entry["time"] = datetime.now().strftime("%H:%M:%S")

        # Create a copy of the entries list, update it with a new key and save the copy to the json file using save_entries
        entries_list = self.entries_list
        entries_list[date_key] = entry
        self.store.save_entries(entries_list)
      
# This function deletes an entry using the date assigned to the entry as a key
    def delete_entry(self, date_key):
        """Delete entry by date"""

        # Create a copy of entries list
        entries_list = self.entries_list
        if date_key in entries_list:
            del entries_list[date_key]
            self.store.save_entries(entries_list)
            return True
        return False

# This function searches for keywords in the content or title of all entries by looping through them, if the content/title contains the pattern, it adds it to the results dictionary
    def search_by_keyword(self, keyword):
        """Search for keyword in titles and content using regex (case-insensitive)"""
        results = []
        # Compile regex pattern (matches partial words too)
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)

        for date_key, entry in self.entries_list.items():
            if pattern.search(entry["title"]) or pattern.search(entry["content"]):
                results.append(entry)

        return results

# This function searches the json list of entries for a particular entry using the date assigned to that entry
    def search_by_date(self, date_key):
        """Search by exact date key"""
        if date_key in self.entries_list:
            return [self.entries_list[date_key]]
        else:
            return []
       
    



diary1 = Diary()
# asssss= diary1.create_entry({
#     "title": "Morning routine",
#     "content": "content ",
#     "date": "07-08-2005"
     
# })


res = diary1.search_by_date("07-08-2005")

print(res)
# print(asssss)