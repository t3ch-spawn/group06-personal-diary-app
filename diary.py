# diary.py
from datetime import datetime
from storage import DiaryStorage
import re

class Diary:
    def __init__(self):
        self.store = DiaryStorage()
        self.users_list = self.store.load_users()
        self.entries_list = self.store.load_users()

# This function creates and edits entries using the date assigned to the entry as a key and passing in the username to update the entries list of the particular user
    def create_entry(self, entry, username):
        """Add a new entry keyed by date (dd-mm-yyyy)"""
        date_key = entry["date"]
        

        # Assign ID based on number of existing entries
        # entry["id"] = len(self.entries_list) + 1
        entry["time"] = datetime.now().strftime("%H:%M:%S")

        # Create a copy of the users_list(basically the json file). 
        users_list = self.users_list

        # Create a copy of the entries of the user with the 'username'
        user_entries = self.store.list_entries(username)

        # Update the entries list of the user with the new entry or edited entry
        user_entries[date_key] = entry

        # Update the entire entries list of the user with the updated entries list above
        users_list[username]['entries'] = user_entries 

        # Save the new and updated user_list to the json file (kind of like replacing it)
        self.store.save_entries(users_list)
      

# This function deletes an entry using the date assigned to the entry as a key and passing in the username to get the list of entries of the user
    def delete_entry(self, date_key, username):
        """Delete entry by date"""

        # Create a copy of the users_list(basically the json file). 
        users_list = self.users_list

        # Create a copy of the entries of the user with the 'username'
        user_entries = self.store.list_entries(username)

        if date_key in user_entries:
            del user_entries[date_key]
            # Update the entire entries list of the users, with the entries of one user deleted
            users_list[username]['entries'] = user_entries 
            self.store.save_entries(users_list)
            return True
        return False

# This function searches for keywords in the content or title of all entries by looping through them, if the content/title contains the pattern, it adds it to the results dictionary
    def search_by_keyword(self, keyword, username):
        """Search for keyword in titles and content using regex (case-insensitive)"""
        results = []
        # Compile regex pattern (matches partial words too)
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)

         # Create a copy of the users_list(basically the json file). 
        users_list = self.users_list

        # Create a copy of the entries of the user with the 'username'
        user_entries = self.store.list_entries(username)
        for date_key, entry in user_entries.items():
            if pattern.search(entry["title"]) or pattern.search(entry["content"]):
                results.append(entry)

        return results

# This function searches the json list of entries for a particular entry using the date assigned to that entry
    def search_by_date(self, search_param, username, type=None):
        """Search by exact date key"""

        # Create a copy of the users_list(basically the json file). 
        users_list = self.users_list

        # Create a copy of the entries of the user with the 'username'
        user_entries = self.store.list_entries(username)

        results = []

        day_pattern = re.compile(rf"\d\d\d\d-\d\d-{re.escape(search_param)}")      # search by month
        month_pattern = re.compile(rf"\d\d\d\d-{re.escape(search_param)}-\d\d")    # search by day
        year_pattern = re.compile(rf"{re.escape(search_param)}-\d\d-\d\d")     #search by year

        for date_key, entry in user_entries.items():
            # print(date_key)
            # If searching by an exact date, i.e "07-04-2005"
            if(search_param == date_key):
                return [user_entries[date_key]]

            # If searching by a particular day, i.e 24, 29, 31
            if(day_pattern.match(date_key) and type=="day"):
                results.append(entry)
                
           
            # If searching by a particular month, i.e 05(May), 01(Jan), 03(March)
            if(month_pattern.match(date_key) and type == 'month'):
                results.append(entry)
                
           
            # If searching by a particular day, i.e 2024, 2022, 2020
            if(year_pattern.match(date_key) and type == 'year'):
                results.append(entry)
                
        return results


