import re


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

# This is a custom exception to throw errors when there is no search result for either a date or a content
class No_Result_Error(Exception):
    def __init__(self, result_type = None, content = None):
        self.message = f"There are no search results for {result_type}: {content}"
        super().__init__(self.message)


    
class Diary():
    def __init__(self, id = None, date = None, time = None, content = None):
        self.id = id
        self.date = date
        self.time = time
        self.content = content
       

  # This function takes the data from the user and creates an entry in a dictionary structure
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "time": self.time,
            "content": self.content,
            "user": self.user
        }

  # This function searches through the available entries for a particular date string, if found, it returns all entries with the date string, if no date is found, it raises a "No Result" error
    def search_by_date(self, date):
        try:
            results = []

            # Loop through the entries array, for each entry if the date matches the date of that particular entry, add that entry to the results list
            for entry in entries["entries"]:
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
      try: 
          # Create a regex pattern by passing in the keyword and ignoring uppercase typography
          pattern = re.compile(re.escape(keyword), re.IGNORECASE)
          results = []

          # Loop through the entries array, for each entry if the pattern matches some part of the content of that particular entry, add that entry to the results list
          for entry in entries["entries"]:
              if pattern.search(entry["content"]):
                  results.append(entry)

          # If the results list length is equal to 0, that means there is no search result, then raise an error
          if(results.__len__() == 0):
               raise No_Result_Error("content", keyword)
          print(results)
          return results
          
      except No_Result_Error as e:
            return e

