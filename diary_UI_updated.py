
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import calendar
from datetime import datetime, date
from typing import Dict, Optional, List
from storage import DiaryStorage
from diary import Diary
import json, os


currUser = {
    "name": ""
}


class DiaryExceptions:
    """Custom exception classes for diary application frontend"""
    
    class UIError(Exception):
        """Raised when UI operations fail"""
        pass
    
    class ValidationError(Exception):
        """Raised when input validation fails"""
        pass
    
    class NavigationError(Exception):
        """Raised when navigation operations fail"""
        pass

class LoginDialog:
    """Frontend username/password authentication dialog"""

    def __init__(self, parent):
        self.parent = parent
        self.success = False
        self.username = ""
        self.password = ""

        # Create login window (1.5x bigger than before)
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Personal Diary - Login")
        self.dialog.geometry("525x420")  # was 350x280
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        # Center the dialog on screen
        self._center_window()

        # Create the login interface
        self._create_login_interface()

        # Handle window closing
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _center_window(self):
        """Centers the login dialog on screen"""
        self.dialog.transient(self.parent)
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (525 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (420 // 2)
        self.dialog.geometry(f"525x420+{x}+{y}")

    def _create_login_interface(self):
        """Creates the login interface elements"""
        # Main container frame
        main_frame = ttk.Frame(self.dialog, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Application title
        title_label = ttk.Label(
            main_frame, text="🔒 Personal Diary",
            font=('Arial', 20, 'bold')
        )
        title_label.pack(pady=(0, 30))

        # Login form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        # Username label and entry
        ttk.Label(form_frame, text="Username:", font=('Arial', 12)).pack(anchor=tk.W, pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, width=40, font=('Arial', 12))
        self.username_entry.pack(fill=tk.X, pady=(0, 15))

        # Password label and entry
        ttk.Label(form_frame, text="Password:", font=('Arial', 12)).pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, show="*", width=40, font=('Arial', 12))
        self.password_entry.pack(fill=tk.X, pady=(0, 15))

        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self._handle_login())

        # Button container
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X)

        # Login button
        login_btn = ttk.Button(
            button_frame, text="Login",
            command=self._handle_login,
            style='Accent.TButton'
        )
        login_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Register new user button
        register_btn = ttk.Button(
            button_frame, text="Register New User",
            command=self._open_register_dialog
        )
        register_btn.pack(side=tk.LEFT)

        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self._on_cancel)
        cancel_btn.pack(side=tk.RIGHT)

        # Focus on username entry
        self.username_entry.focus()

    def _handle_login(self):
        """Handles login with JSON file validation"""
        self.username = self.username_entry.get().strip()
        self.password = self.password_entry.get().strip()

        if not self.username or not self.password:
            messagebox.showerror("Login Error", "Please enter both username and password!")
            return

        try:
            with open("diary.json", "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Login Error", "User does not exist")
            return

        # Check if user exists
        if self.username not in users:
            messagebox.showerror("Login Error", "User does not exist!")
            return

        # Validate password
        stored_password = users[self.username]["password"]
        if self.password == stored_password:
            self.success = True
            messagebox.showinfo("Success", "Login successful!")
            currUser["name"] = self.username
            self.dialog.destroy()
        else:
            messagebox.showerror("Login Error", "Incorrect password!")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def _open_register_dialog(self):
        """Opens a dialog for registering a new user"""
        reg_dialog = tk.Toplevel(self.dialog)
        reg_dialog.title("Register New User")
        width, height = 400, 320
        reg_dialog.geometry(f"{width}x{height}")
        reg_dialog.resizable(False, False)
        reg_dialog.transient(self.dialog)
        reg_dialog.grab_set()

        # Center the dialog
        reg_dialog.update_idletasks()
        x = (reg_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (reg_dialog.winfo_screenheight() // 2) - (height // 2)
        reg_dialog.geometry(f"{width}x{height}+{x}+{y}")
        

        frame = ttk.Frame(reg_dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Create Username:", font=('Arial', 11)).pack(anchor=tk.W, pady=(0, 5))
        username_entry = ttk.Entry(frame, width=30, font=('Arial', 11))
        username_entry.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(frame, text="Create Password:", font=('Arial', 11)).pack(anchor=tk.W, pady=(0, 5))
        password_entry = ttk.Entry(frame, show="*", width=30, font=('Arial', 11))
        password_entry.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(frame, text="Confirm Password:", font=('Arial', 11)).pack(anchor=tk.W, pady=(0, 5))
        confirm_entry = ttk.Entry(frame, show="*", width=30, font=('Arial', 11))
        confirm_entry.pack(fill=tk.X, pady=(0, 15))

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        def handle_register():
                """UI-only password match check"""
                if password_entry.get() != confirm_entry.get():
                    messagebox.showerror("Error", "Passwords do not match!")
                else:
                    username = username_entry.get().strip()

                    users = {}
                    if os.path.exists("diary.json"):
                        with open("diary.json", "r") as f:
                            try:
                                users = json.load(f)
                            except json.JSONDecodeError:
                                users = {}

                    if username in users:
                        messagebox.showerror("Error", f"User '{username}' already exists!")
                        return

                messagebox.showinfo("Success", "User registered.")
                store1 = DiaryStorage()
                store1.add_user(username, password_entry.get())
                reg_dialog.destroy()

        ttk.Button(btn_frame, text="Register", command=handle_register).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancel", command=reg_dialog.destroy).pack(side=tk.RIGHT)

    def _on_cancel(self):
        """Handles dialog cancellation"""
        self.success = False
        self.parent.destroy()  


class CalendarWidget:
    """Custom calendar widget for intuitive date navigation"""
    
    def __init__(self, parent, date_callback):
        self.parent = parent
        self.date_callback = date_callback  # Callback when date is selected
        self.current_date = datetime.now()
        self.selected_date = date.today()
        
        # Store day buttons for styling
        self.day_buttons = {}
        
        self._create_calendar_interface()
        self._update_calendar_display()
    
    def _create_calendar_interface(self):
        """Creates the calendar interface structure"""
        # Main calendar container
        self.frame = ttk.LabelFrame(self.parent, text="📅 Calendar Navigation", 
                                   padding="15",)
        
        # Navigation header
        nav_frame = ttk.Frame(self.frame)
        nav_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Previous month button
        self.prev_button = ttk.Button(nav_frame, text="◀", width=3,
                                     command=self._navigate_previous_month)
        self.prev_button.pack(side=tk.LEFT)
        
        # Month/Year display
        self.month_year_label = ttk.Label(nav_frame, font=('Arial', 14, 'bold'))
        self.month_year_label.pack(side=tk.LEFT, expand=True)
        
        # Next month button
        self.next_button = ttk.Button(nav_frame, text="▶", width=3,
                                     command=self._navigate_next_month)
        self.next_button.pack(side=tk.RIGHT)
        
        # Calendar grid container
        self.calendar_grid = ttk.Frame(self.frame, width=800)
        self.calendar_grid.pack()
        
        # Today button for quick navigation
        today_frame = ttk.Frame(self.frame)
        today_frame.pack(fill=tk.X, pady=(15, 0))
        
        today_btn = ttk.Button(today_frame, text="📍 Go to Today", 
                              command=self._go_to_today)
        today_btn.pack()
    
    def _navigate_previous_month(self):
        """Navigates to the previous month"""
        try:
            if self.current_date.month == 1:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year - 1, month=12)
            else:
                self.current_date = self.current_date.replace(
                    month=self.current_date.month - 1)
            self._update_calendar_display()
        except Exception as e:
            raise DiaryExceptions.NavigationError(f"Failed to navigate to previous month: {e}")
    
    def _navigate_next_month(self):
        """Navigates to the next month"""
        try:
            if self.current_date.month == 12:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year + 1, month=1)
            else:
                self.current_date = self.current_date.replace(
                    month=self.current_date.month + 1)
            self._update_calendar_display()
        except Exception as e:
            raise DiaryExceptions.NavigationError(f"Failed to navigate to next month: {e}")
    
    def _go_to_today(self):
        """Quick navigation to today's date"""
        self.current_date = datetime.now()
        self.selected_date = date.today()
        self._update_calendar_display()
        self.date_callback(self.selected_date)
    
    def _update_calendar_display(self):
        """Updates the calendar display with current month"""
        # Clear existing calendar
        for widget in self.calendar_grid.winfo_children():
            widget.destroy()
        self.day_buttons.clear()
        
        # Update month/year label
        month_name = calendar.month_name[self.current_date.month]
        self.month_year_label.config(text=f"{month_name} {self.current_date.year}")
        
        # Create day headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for col, day in enumerate(days):
            header = ttk.Label(self.calendar_grid, text=day, 
                              font=('Arial', 10, 'bold'))
            header.grid(row=0, column=col, padx=2, pady=2, sticky='nsew')
        
        # Get calendar matrix for current month
        cal_matrix = calendar.monthcalendar(self.current_date.year, 
                                           self.current_date.month)
        
        # Create day buttons
        today = date.today()
        for week_num, week in enumerate(cal_matrix, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty space for days from adjacent months
                    spacer = ttk.Label(self.calendar_grid, text="")
                    spacer.grid(row=week_num, column=day_num, padx=2, pady=2)
                else:
                    # Create clickable day button
                    button_date = date(self.current_date.year, 
                                     self.current_date.month, day)
                    
                    # Style button based on state
                    button_text = str(day)
                    if button_date == today:
                        button_text = f"[{day}]"  # Mark today
                    
                    day_button = ttk.Button(self.calendar_grid, text=button_text, 
                                          width=3,
                                          command=lambda d=button_date: self._select_date(d))
                    day_button.grid(row=week_num, column=day_num, padx=1, pady=1, 
                                  sticky='nsew')
                    
                    # Store button reference
                    self.day_buttons[button_date] = day_button
                    
                    # Highlight selected date
                    if button_date == self.selected_date:
                        day_button.configure(style='Accent.TButton')
    
    def _select_date(self, selected_date):
        """Handles date selection"""
        self.selected_date = selected_date
        self._update_calendar_display()  # Refresh to show selection
        self.date_callback(selected_date)  # Notify parent component
    
    def pack(self, **kwargs):
        """Packs the calendar frame"""
        self.frame.pack(**kwargs)

        
        


class EntriesViewer:
    """Window to display all diary entries in list format (robust and clickable)"""

    def __init__(self, parent, entries, open_callback=None):
        store1 = DiaryStorage()
        self.parent = parent
        self.entries = store1.list_entries(currUser["name"])  # expected to be dict keyed by "YYYY-MM-DD"
        self.open_callback = open_callback
        self.ascending = True
        self.id_map = {}  # map tree iid -> date_key


        # Create viewer window
        self.window = tk.Toplevel(parent)
        self.window.title("📋 All Diary Entries")
        width, height = 640, 420
        self.window.geometry(f"{width}x{height}")
        self.window.transient(parent)
        self.window.grab_set()

        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        

        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for entries
        self.tree = ttk.Treeview(
            main_frame,
            columns=("Date", "Title", "Content"),
            show="headings",
            height=14
        )

        self.tree.heading("Date", text="Date")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Content", text="Content")

        self.tree.column("Date", width=110, anchor=tk.CENTER)
        self.tree.column("Title", width=100, anchor=tk.CENTER)
        self.tree.column("Content", width=380, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind double click AFTER tree is created
        self.tree.bind("<Double-1>", self._open_selected_entry)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(fill=tk.X, pady=8)

        open_btn = ttk.Button(btn_frame, text="Open Selected", command=self._open_selected_entry)
        open_btn.pack(side=tk.LEFT, padx=6)

        toggle_btn = ttk.Button(btn_frame, text="⇅ Toggle Order", command=self.toggle_order)
        toggle_btn.pack(side=tk.LEFT, padx=6)

        close_btn = ttk.Button(btn_frame, text="Close", command=self.window.destroy)
        close_btn.pack(side=tk.RIGHT, padx=6)

        # Load entries initially
        self.load_entries()

    def load_entries(self):
        """Load entries into the treeview with stable iids and an id_map"""
        # clear previous
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.id_map.clear()

        # Build sorted list of entries (entries is a dict of date_key -> MockDiaryEntry)
        sorted_entries = sorted(
            self.entries.values(),
            key=lambda e: datetime.strptime(e['date'], "%Y-%m-%d"),
            reverse=not self.ascending
        )

        def preview_text(text, limit=10):
            return text[:limit] + "..." if len(text) > limit else text

        # Insert with sequential iids and store mapping to date_key
        for idx, entry in enumerate(sorted_entries):
            dt = datetime.strptime(entry['date'], "%Y-%m-%d")
            iid = str(idx)
            self.id_map[iid] = entry['date']  # date_key (YYYY-MM-DD)
            self.tree.insert(
                "",
                tk.END,
                iid=iid,
                values=(dt.strftime("%Y-%m-%d"), preview_text(entry['title'], 8) or "Untitled", preview_text(entry['content'], 20))
            )

    def toggle_order(self):
        self.ascending = not self.ascending
        self.load_entries()

    def _open_selected_entry(self, event=None):
        """Open the selected diary entry using the provided callback (if any)"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Selection", "Please select an entry to open!")
            return

        iid = selection[0]
        date_key = self.id_map.get(iid)
        if not date_key:
            messagebox.showerror("Error", "Could not resolve selected entry.")
            return

        # If the caller provided an open_callback, call it with a date object
        if self.open_callback:
            try:
                parsed_date = datetime.strptime(date_key, "%Y-%m-%d").date()
                self.open_callback(parsed_date)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open entry: {e}")
        else:
            messagebox.showinfo("Info", "No open callback provided by the application.")
        self.window.destroy()




class SearchDialog:
    """Search dialog for finding diary entries"""
    
    def __init__(self, parent, search_callback):
        self.parent = parent
        self.search_callback = search_callback
        
        # Create search dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🔍 Search Diary Entries")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self._center_dialog()
        
        # Create search interface
        self._create_search_interface()
    
    def _center_dialog(self):
        """Centers the search dialog"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
    
    def _create_search_interface(self):
        """Creates the search interface"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search input section
        search_frame = ttk.LabelFrame(main_frame, text="Search Parameters", 
                                     padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(search_frame, text="Search term:", 
                 font=('Arial', 11)).pack(anchor=tk.W)
        
        self.search_entry = ttk.Entry(search_frame, font=('Arial', 11))
        self.search_entry.pack(fill=tk.X, pady=(5, 10))
        self.search_entry.bind('<Return>', lambda e: self._perform_search())
        
        # Search options
        options_frame = ttk.Frame(search_frame)
        options_frame.pack(fill=tk.X)
        
        self.search_option = tk.StringVar(value="titleContent")
        
        # First row frame
        row1 = ttk.Frame(options_frame)
        row1.pack(fill=tk.X, pady=5)

        ttk.Radiobutton(row1, text="Search for titles and content", 
                       variable=self.search_option, value="titleContent").pack(side=tk.LEFT)
        ttk.Radiobutton(row1, text="Search for dates (format: 2025-04-31)", 
                       variable=self.search_option, value="date").pack(side=tk.LEFT, padx=(20, 0))

        # Second row frame
        row2 = ttk.Frame(options_frame)
        row2.pack(fill=tk.X, pady=5)

        ttk.Radiobutton(row2, text="Search for day (format: 31)", 
                       variable=self.search_option, value="day").pack(side=tk.LEFT)
        ttk.Radiobutton(row2, text="Search for month (format: 05)", 
                       variable=self.search_option, value="month").pack(side=tk.LEFT, padx=(20, 0))
        
         # Third row frame
        row3 = ttk.Frame(options_frame)
        row3.pack(fill=tk.X, pady=5)    
        ttk.Radiobutton(row3, text="Search for year (format: 2025)", 
               variable=self.search_option, value="year").pack(side=tk.LEFT)
        
        # Search button
        ttk.Button(search_frame, text="🔍 Search", 
                  command=self._perform_search).pack(pady=(10, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Search Results", 
                                      padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results treeview
        self.results_tree = ttk.Treeview(results_frame, 
                                        columns=('Date', 'Title', 'Preview'),
                                        show='tree headings', height=10)
        
        # Configure columns
        self.results_tree.heading('#0', text='#')
        self.results_tree.heading('Date', text='Date')
        self.results_tree.heading('Title', text='Title')
        self.results_tree.heading('Preview', text='Content Preview')
        
        self.results_tree.column('#0', width=40)
        self.results_tree.column('Date', width=100)
        self.results_tree.column('Title', width=120)
        self.results_tree.column('Preview', width=200)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL,
                                 command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to open entry
        self.results_tree.bind('<Double-1>', self._open_selected_entry)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(button_frame, text="Open Selected", 
                  command=self._open_selected_entry).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Close", 
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # Focus on search entry
        self.search_entry.focus()
    
    def _perform_search(self):
        """Performs the search operation - Frontend simulation"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Search", "Please enter a search term!")
            return
        
        if not (self.search_option.get()):
            messagebox.showwarning("Search", "Please select at least one search option!")
            return
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        diary1 = Diary()

        search_choice = self.search_option.get()

        if(search_choice == "titleContent"):
            results = diary1.search_by_keyword(search_term, currUser["name"])
        elif(search_choice == "date"):
            results = diary1.search_by_date(search_term, currUser["name"])
        elif(search_choice == "month"):
            results = diary1.search_by_date(search_term, currUser["name"], "month")
        elif(search_choice == "day"):
            results = diary1.search_by_date(search_term, currUser["name"], "day")
        elif(search_choice == "year"):
            results = diary1.search_by_date(search_term, currUser["name"], "year")

        # Mock search results for demonstration
        # mock_results = [
        #     {"date": "2024-01-15", "title": "Morning Thoughts", 
        #      "preview": f"Found '{search_term}' in this entry about daily reflections..."},
        #     {"date": "2024-02-03", "title": "Weekend Adventures", 
        #      "preview": f"This entry contains '{search_term}' and describes outdoor activities..."},
        #     {"date": "2024-02-20", "title": "", 
        #      "preview": f"Untitled entry with '{search_term}' mentioned in the content..."}
        # ]
        
        # Populate results
        for i, result in enumerate(results, 1):
            self.results_tree.insert('', tk.END, 
                                   text=str(i),
                                   values=(result['date'], 
                                          result['title'] or 'Untitled',
                                          result['content']))
        
        messagebox.showinfo("Search Complete", f"Found {len(results)} entries!")
    
    def _open_selected_entry(self, event=None):
        """Opens the selected search result"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showinfo("Selection", "Please select an entry to open!")
            return
        
        # Get selected entry data
        item = self.results_tree.item(selection[0])
        entry_date = item['values'][0]
        
        # Parse date and callback to main application
        try:
            parsed_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
            self.search_callback(parsed_date)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format in search results!")


class DiaryMainInterface:
    """Main diary application interface"""
    
    def __init__(self):
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("📔 Personal Diary Application")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Current state variables
        self.current_date = None
        self.is_modified = False
        self.is_saving = False  # Flag to prevent concurrent operations
        self.mock_entries = {}  # Mock data storage for frontend demo
        self.action_buttons = {}  # Initialize action_buttons dictionary
        
        # Configure styles
        self._configure_styles()
        
        # Show login dialog
        if not self._handle_authentication():
            self.root.destroy()
            return
        
        # Create main interface
        self._create_main_interface()
        
        # Initialize with today's date
        self._load_date_entry(date.today())
    
    def _configure_styles(self):
        """Configures custom styles for the interface"""
        style = ttk.Style()
        style.theme_use('clam')  # Use modern theme
        
        # Configure custom button styles
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        style.configure('Calendar.TButton', font=('Arial', 9))
    
    def _handle_authentication(self):
        """Handles user authentication through login dialog"""
        login_dialog = LoginDialog(self.root)
        self.root.wait_window(login_dialog.dialog)
        
        # if login_dialog.success:
        #     messagebox.showinfo("Welcome", 
        #                       f"Welcome to your personal diary!\nPassword set: {login_dialog.password}")
        #     return True
        
        return True
        # return False
    
    def _create_main_interface(self):
        """Creates the main application interface"""
        # Create menu bar
        self._create_menu_bar()
        
        # Create main layout
        self._create_layout()
        
        # Setup event handlers
        self._setup_event_handlers()
    
    def _create_menu_bar(self):
        """Creates the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label=" Export Diary", command=self._export_diary)
        file_menu.add_command(label="📥 Import Entries", command=self._import_entries)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self._handle_exit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="✏️ Edit", menu=edit_menu)
        edit_menu.add_command(label="📋 Copy Text", command=self._copy_text,
                             accelerator="Ctrl+C")
        edit_menu.add_command(label="📄 Paste Text", command=self._paste_text,
                             accelerator="Ctrl+V")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ View", menu=view_menu)
        view_menu.add_command(label="📅 Go to Today", command=self._go_to_today)
        view_menu.add_command(label="📈 Entry Statistics", command=self._show_statistics)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="🎯 Quick Tutorial", command=self._show_tutorial)
        help_menu.add_command(label="🔧 Keyboard Shortcuts", command=self._show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ About", command=self._show_about)
    
    def _create_layout(self):
        """Creates the main application layout"""
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Calendar and quick actions
        left_panel = ttk.Frame(main_container, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)  # Maintain fixed width
        
        # Calendar widget
        self.calendar_widget = CalendarWidget(left_panel, self._on_date_selected)
        self.calendar_widget.pack(fill=tk.X, pady=(0, 15))
        
        # Quick actions panel
        self._create_quick_actions(left_panel)
        
        # Right panel - Entry editor
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self._create_entry_editor(right_panel)
    
    def _create_quick_actions(self, parent):
        """Creates quick action buttons panel"""
        actions_frame = ttk.LabelFrame(parent, text="⚡ Quick Actions", padding="10")
        actions_frame.pack(fill=tk.X, pady=(0, 15))
        store1 = DiaryStorage()
        buttons = [
    ("💾 Save", self._save_current_entry),
    ("🔍 Search", self._show_search_dialog),
    # ("✏️ Edit", self._edit_current_entry),
    ("🗑️ Delete", self._delete_current_entry),
    ("📅 Today", self._go_to_today),
    ("📋 View All", lambda: EntriesViewer(self.root, store1.list_entries(currUser["name"]), self._load_date_entry))
]
        
        # Create and store button references
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(actions_frame, text=text, command=command, width=15)
            row, col = divmod(i, 2)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
            self.action_buttons[text] = btn  # Store button reference
            
        # Initially disable edit and delete buttons
        self._update_button_states(is_new_entry=True)
        
        # Configure grid weights
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
    
    def _create_entry_editor(self, parent):
        """Creates the diary entry editor section"""
        # Header section
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Date display
        self.date_display = ttk.Label(header_frame, text="Select a date to begin", 
                                     font=('Arial', 16, 'bold'))
        self.date_display.pack(anchor=tk.W)
        
        # Entry title section
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="📝 Entry Title (Optional):", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        
        self.title_entry = ttk.Entry(title_frame, font=('Arial', 12))
        self.title_entry.pack(fill=tk.X, pady=(5, 0))
        self.title_entry.bind('<KeyRelease>', self._on_content_modified)
        
        # Content editor section
        editor_frame = ttk.LabelFrame(parent, text="📖 Diary Content", padding="10")
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text editor with scrollbar
        text_container = ttk.Frame(editor_frame)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        # Text widget
        self.text_editor = tk.Text(text_container, 
                                  wrap=tk.WORD, 
                                  font=('Arial', 12),
                                  undo=True, 
                                  maxundo=50,
                                  relief=tk.FLAT,
                                  borderwidth=5,
                                  padx=10,
                                  pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL,
                                   command=self.text_editor.yview)
        h_scrollbar = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL,
                                   command=self.text_editor.xview)
        
        self.text_editor.configure(yscrollcommand=v_scrollbar.set,
                                  xscrollcommand=h_scrollbar.set)
        
        # Pack text widget and scrollbars
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind content change events
        self.text_editor.bind('<KeyRelease>', self._on_content_modified)
        self.text_editor.bind('<Button-1>', self._on_content_modified)
        
        # Status bar
        self._create_status_bar(parent)
    
    def _create_status_bar(self, parent):
        """Creates the status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready", 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Word count label
        self.word_count_label = ttk.Label(status_frame, text="Words: 0", 
                                         relief=tk.SUNKEN, width=15)
        self.word_count_label.pack(side=tk.RIGHT)
    
    def _setup_event_handlers(self):
        """Sets up event handlers and keyboard shortcuts"""
        # Keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self._save_current_entry())
        self.root.bind('<Control-f>', lambda e: self._show_search_dialog())
        self.root.bind('<Control-n>', lambda e: self._clear_current_entry())
        self.root.bind('<Delete>', lambda e: self._delete_current_entry())
        
        # Window closing event
        self.root.protocol("WM_DELETE_WINDOW", self._handle_exit)
        
        # Text editor specific bindings
        self.text_editor.bind('<Control-a>', self._select_all_text)
    
    def _on_date_selected(self, selected_date):
        """Handles date selection from calendar"""
        # Check if current entry needs saving
        if self.is_modified and self.current_date:
            result = messagebox.askyesnocancel(
                "Unsaved Changes", 
                "You have unsaved changes. Do you want to save them?")
            
            if result is True:  # Yes - save changes
                self._save_current_entry()
            elif result is None:  # Cancel - don't change date
                return
            # If No (False), continue without saving
        
        # Load the selected date
        self._load_date_entry(selected_date)
    
    def _update_button_states(self, is_new_entry=False):
        """Updates the state of edit and delete buttons based on entry state"""
        try:
            edit_btn = self.action_buttons.get("✏️ Edit")
            delete_btn = self.action_buttons.get("🗑️ Delete")

            if is_new_entry or not self.current_date:
                # Disable edit and delete buttons for new entries
                if edit_btn:
                    edit_btn.config(state='disabled')
                if delete_btn:
                    delete_btn.config(state='disabled')
            else:
                # Enable edit and delete buttons for existing entries
                if edit_btn:
                    edit_btn.config(state='normal')
                if delete_btn:
                    delete_btn.config(state='normal')
        except Exception as e:
            print(f"Button state update error: {e}")
            messagebox.showerror("Error", "Failed to update button states")
    
    def _load_date_entry(self, entry_date):
        """Loads diary entry for the specified date"""
        self.current_date = entry_date
        
        # Update date display
        formatted_date = entry_date.strftime("%A, %B %d, %Y")
        self.date_display.config(text=f"📅 {formatted_date}")
        
        # Load entry data (mock data for frontend demo)
        date_key = entry_date.strftime("%Y-%m-%d")
        
        store1 = DiaryStorage()
        entries_list = store1.list_entries(currUser["name"])

        if date_key in entries_list:
            entry = entries_list[date_key]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, entry['title'])
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, entry['content'])
            self.status_label.config(text=f"Loaded entry from {formatted_date}")
            self._update_button_states(is_new_entry=False)
        else:
            # Clear for new entry
            self.title_entry.delete(0, tk.END)
            self.text_editor.delete(1.0, tk.END)
            self.status_label.config(text=f"New entry for {formatted_date}")
            self._update_button_states(is_new_entry=True)
        
        # Reset modification flag
        self.is_modified = False
        self._update_word_count()
    
    def _on_content_modified(self, event=None):
        """Handles content modification events"""
        if not self.is_modified:
            self.is_modified = True
            self.status_label.config(text="Modified - Remember to save your changes!")
        
        self._update_word_count()
    
    def _update_word_count(self):
        """Updates the word count display"""
        content = self.text_editor.get(1.0, tk.END).strip()
        word_count = len(content.split()) if content else 0
        self.word_count_label.config(text=f"Words: {word_count}")
    
    def _edit_current_entry(self):
        """Enables editing of the current diary entry"""
        if not self.current_date:
            messagebox.showwarning("No Date Selected", "Please select a date first!")
            return
        store1 = DiaryStorage()
        entries_list = store1.list_entries(currUser["name"])
        date_key = self.current_date.strftime("%Y-%m-%d")
        if date_key not in entries_list:
            messagebox.showinfo("No Entry", "No entry exists for this date to edit!")
            return

        # Enable text editor and title entry if they were disabled
        self.title_entry.config(state='normal')
        self.text_editor.config(state='normal')
        
        # Set focus to the title entry
        self.title_entry.focus()
        
        # Update status
        self.status_label.config(text="✏️ Editing entry - Remember to save your changes!")
        self.is_modified = True

    def _save_current_entry(self):
        """Saves the current diary entry"""
        if self.is_saving:
            messagebox.showinfo("Please Wait", "Save operation in progress...")
            return
            
        if not self.current_date:
            messagebox.showwarning("No Date Selected", "Please select a date first!")
            return
            
        self.is_saving = True  # Set saving flag
        
        # Get current content
        title = self.title_entry.get().strip()
        content = self.text_editor.get(1.0, tk.END).strip()
        
        # Check if there's any actual content (ignoring whitespace)
        if not content:
            if not title:
                messagebox.showinfo("Nothing to Save", "Entry is empty!")
                return
            # If there's only a title, confirm with user
            if not messagebox.askyesno("Save Entry", "Save entry with only title and no content?"):
                return
        
        # Save to mock storage
        date_key = self.current_date.strftime("%Y-%m-%d")
        diary1 = Diary()
        diary1.create_entry( {
             "title": title,
            "content": content,
             "date": date_key
        }, currUser["name"])

        # self.mock_entries[date_key] = MockDiaryEntry(date_key, content, title)
        
        try:
            # Update UI
            self.is_modified = False
            formatted_date = self.current_date.strftime("%B %d, %Y")
            self.status_label.config(text=f"✅ Entry saved for {formatted_date}")
            
            # Enable edit and delete buttons after saving
            self._update_button_states(is_new_entry=False)
            
            messagebox.showinfo("Save Successful", f"Entry saved for {formatted_date}!")
        finally:
            self.is_saving = False  # Reset saving flag
    
    def _delete_current_entry(self):
        """Deletes the current diary entry"""
        store1 = DiaryStorage()
        entries_list = store1.list_entries(currUser["name"])
        try:
            if not self.current_date:
                messagebox.showwarning("No Date Selected", "Please select a date first!")
                return
            
            date_key = self.current_date.strftime("%Y-%m-%d")
            
            if date_key not in entries_list:
                messagebox.showinfo("No Entry", "No entry exists for this date!")
                return
            
            # Save the entry temporarily in case we need to restore it
            temp_entry = entries_list[date_key]
            
            # Confirm deletion
            formatted_date = self.current_date.strftime("%B %d, %Y")
            result = messagebox.askyesno("Confirm Deletion", 
                                       f"Are you sure you want to delete the entry for {formatted_date}?")
            
            diary1 = Diary()
            if result:
                try:
                    # Attempt deletion
                    # del entries_list[date_key]
                    diary1.delete_entry(date_key, currUser["name"])
                    self.title_entry.delete(0, tk.END)
                    self.text_editor.delete(1.0, tk.END)
                    self.is_modified = False
                    self.status_label.config(text=f"🗑️ Entry deleted for {formatted_date}")
                    messagebox.showinfo("Delete Successful", f"Entry deleted for {formatted_date}!")
                    
                    # Update button states after successful deletion
                    self._update_button_states(is_new_entry=True)
                except Exception as e:
                    # Restore the entry if deletion fails
                    self.entries_list[date_key] = temp_entry
                    raise Exception(f"Failed to delete entry: {str(e)}")
                    
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))
            print(f"Delete error: {e}")
    
    def _clear_current_entry(self):
        """Clears the current entry editor"""
        if self.is_modified:
            result = messagebox.askyesno("Clear Entry", 
                                       "Are you sure you want to clear the current entry? Unsaved changes will be lost!")
            if not result:
                return
        
        self.title_entry.delete(0, tk.END)
        self.text_editor.delete(1.0, tk.END)
        self.is_modified = False
        self.status_label.config(text="Entry cleared")
    
    def _show_search_dialog(self):
        """Shows the search dialog"""
        SearchDialog(self.root, self._on_search_result_selected)
    
    def _on_search_result_selected(self, result_date):
        """Handles search result selection"""
        # Update calendar to show the selected month
        self.calendar_widget.current_date = datetime(result_date.year, result_date.month, 1)
        self.calendar_widget._update_calendar_display()
        
        # Load the entry for the selected date
        self._load_date_entry(result_date)
    
    def _go_to_today(self):
        """Navigates to today's date"""
        today = date.today()
        self.calendar_widget.current_date = datetime.now()
        self.calendar_widget.selected_date = today
        self.calendar_widget._update_calendar_display()
        self._load_date_entry(today)
    
    def _copy_text(self):
        """Copies selected text to clipboard"""
        try:
            self.text_editor.event_generate("<<Copy>>")
            self.status_label.config(text="Text copied to clipboard")
        except Exception:
            messagebox.showerror("Copy Error", "Failed to copy text!")
    
    def _paste_text(self):
        """Pastes text from clipboard"""
        try:
            self.text_editor.event_generate("<<Paste>>")
            self._on_content_modified()
            self.status_label.config(text="Text pasted from clipboard")
        except Exception:
            messagebox.showerror("Paste Error", "Failed to paste text!")
    
    def _select_all_text(self, event):
        """Selects all text in the editor"""
        self.text_editor.tag_add(tk.SEL, "1.0", tk.END)
        self.text_editor.mark_set(tk.INSERT, "1.0")
        self.text_editor.see(tk.INSERT)
        return 'break'
    
    def _export_diary(self):
        """Mock export functionality"""
        messagebox.showinfo("Export", "Export functionality would save your diary to a file!\n(Frontend demonstration)")
    
    def _import_entries(self):
        """Mock import functionality"""
        messagebox.showinfo("Import", "Import functionality would load entries from a file!\n(Frontend demonstration)")
    
    def _show_statistics(self):
        """Shows diary statistics"""
        store1 = DiaryStorage()
        entries_list = store1.list_entries(currUser["name"])
        total_entries = len(entries_list)
        total_words = sum(len(entry['content'].split()) for entry in entries_list.values())
        
        stats_msg = f"""📊 Diary Statistics:
        
📝 Total Entries: {total_entries}
📖 Total Words: {total_words}
⭐ Average Words per Entry: {total_words // max(total_entries, 1)}
📅 Date Range: {len(entries_list)} days with entries"""
        
        messagebox.showinfo("Diary Statistics", stats_msg)
    
    def _show_tutorial(self):
        """Shows quick tutorial"""
        tutorial_msg = """🎯 Quick Tutorial:
        
1️⃣ Click on calendar dates to navigate
2️⃣ Type your diary entry in the text area
3️⃣ Add an optional title
4️⃣ Press Ctrl+S or click Save to save
5️⃣ Use Ctrl+F to search your entries
6️⃣ Use the quick action buttons for common tasks
        
💡 Tip: The app will remind you to save unsaved changes!"""
        
        messagebox.showinfo("Quick Tutorial", tutorial_msg)
    
    def _show_shortcuts(self):
        """Shows keyboard shortcuts"""
        shortcuts_msg = """⌨️ Keyboard Shortcuts:
        
💾 Ctrl+S - Save current entry
🔍 Ctrl+F - Search entries  
📋 Ctrl+C - Copy selected text
📄 Ctrl+V - Paste text
🆕 Ctrl+N - Clear current entry
🗑️ Del - Delete current entry
📝 Ctrl+A - Select all text"""
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_msg)
    
    def _show_about(self):
        """Shows about dialog"""
        about_msg = """📔 Personal Diary Application
        
Version: 1.0 (Frontend Demo)
Created with: Python & Tkinter
        
Features:
✅ Intuitive calendar navigation
✅ Rich text editing
✅ Search functionality  
✅ Clean, modern interface
✅ Keyboard shortcuts
✅ Entry management
        
This is a frontend demonstration showcasing
the user interface design and interactions."""
        
        messagebox.showinfo("About Personal Diary", about_msg)
    
    def _handle_exit(self):
        """Handles application exit"""
        if self.is_modified:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before exiting?")
            
            if result is True:  # Yes - save and exit
                self._save_current_entry()
            elif result is None:  # Cancel - don't exit
                return
        
        # Show goodbye message
        messagebox.showinfo("Goodbye", "Thank you for using Personal Diary!\n📔✨")
        self.root.destroy()
    
    def run(self):
        """Runs the diary application"""
        self.root.mainloop()


def main():
    """Main function to start the diary application"""
    try:
        app = DiaryMainInterface()
        app.run()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start diary application:\n{e}")


if __name__ == "__main__":
    main()

