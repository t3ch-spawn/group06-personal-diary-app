from storage import DiaryStorage

# Create diary object
diary = DiaryStorage()

# Add dummy entries
diary.add_entry("First Day", "my first day at work!")
diary.add_entry("Second Day", "this shit is hard fr, type shii.")

# Show entries
print("\nAll diary entries:\n")
diary.list_entries()
