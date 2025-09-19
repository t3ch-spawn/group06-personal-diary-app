import re
from storage import DiaryStorage



# This is a custom exception to throw errors when there is no search result for either a date or a content
class No_Result_Error(Exception):
    def __init__(self, result_type = None, content = None):
        self.message = f"There are no search results for {result_type}: {content}"
        super().__init__(self.message)


diaryStore = DiaryStorage()   
class Diary():
    def __init__(self, id = None, date = None, time = None, content = None):
        self.id = id
        self.date = date
        self.time = time
        self.content = content
       

  # This function takes the data from the user and creates an entry in a dictionary structure
    def create_entry(self, entry):
        entries = diaryStore.list_entries()
        entry_id =  entries[-1]["id"] + 1 if len(entries) > 0 else 1
        entries.append({
            "id": entry_id,
            "date": entry["date"],
            "time": entry["time"],
            "content": entry["content"],
            "title": entry["title"]
        })
        diaryStore.save_entries(entries)
    
    def edit_entry(self, entry_id, new_entry=None):
       entries = diaryStore.list_entries()
       for entry in entries:
           if entry["id"] == entry_id:
               entry.update(new_entry)
       
       diaryStore.save_entries(entries)
       return entries
                    
                
  

    def delete_entry(self, entry_id):
        entries = diaryStore.list_entries()
        for entry in entries:
            if entry["id"] == entry_id:
                entries.remove(entry)
        diaryStore.save_entries(entries)
                   
   

  # This function searches through the available entries for a particular date string, if found, it returns all entries with the date string, if no date is found, it raises a "No Result" error
    def search_by_date(self, date):
        entries = diaryStore.list_entries()
        try:
            results = []

            # Loop through the entries array, for each entry if the date matches the date of that particular entry, add that entry to the results list
            for entry in entries:
                if(entry["date"] == date):
                    results.append(entry)

            # If the results list length is equal to 0, that means there is no search result, then raise an error
            if(results.__len__() == 0):
               raise No_Result_Error("date", date)
            return results
        except No_Result_Error as e:
            return e

  # This function searches for content of an entry through a keyword(which is the user input), using regex
    def search_by_keyword(self, keyword):
      entries = diaryStore.list_entries()
      try: 
          # Create a regex pattern by passing in the keyword and ignoring uppercase typography
          pattern = re.compile(re.escape(keyword), re.IGNORECASE)
          results = []

          # Loop through the entries array, for each entry if the pattern matches some part of the content or title of that particular entry, add that entry to the results list
          for entry in entries:
              if pattern.search(entry["content"]) or pattern.search(entry["title"]):
                  results.append(entry)

          # If the results list length is equal to 0, that means there is no search result, then raise an error
          if(results.__len__() == 0):
               raise No_Result_Error("content", keyword)
          print(results)
          return results
          
      except No_Result_Error as e:
            return e



diary1 = Diary()

# diary1.delete_entry(2)
diary1.create_entry(  {
        "date": "25-06-2025",
        "time": "11:00",
        "content": "Worked for noth stronger.",
        "title": "MY day in the life",
    })


# currEntries = diaryStore.list_entries()
# print(currEntries)