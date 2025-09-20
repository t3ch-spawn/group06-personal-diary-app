
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import calendar
from datetime import datetime, date
from typing import Dict, Optional, List
from storage import DiaryStorage
from diary import Diary
try:
    from src.security import DiaryLock, DiaryLockedError
except ImportError:
    from security import DiaryLock, DiaryLockedError
import json
import os

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


class UserStorage:
    """Manages user credentials and authentication"""
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = {}
        self._load_users()
    
    def _load_users(self):
        """Load users from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.users = json.load(f)
        except Exception as e:
            raise DiaryExceptions.UIError(f"Failed to load users: {e}")
    
    def _save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.users, f, indent=4)
        except Exception as e:
            raise DiaryExceptions.UIError(f"Failed to save users: {e}")
    
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user and initialize their diary"""
        if username in self.users:
            raise DiaryExceptions.ValidationError("Username already exists!")
            
        # Create user record
        self.users[username] = {
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "diary_file": f"diary_{username}.json"  # Each user gets their own diary file
        }
        self._save_users()
        
        # Initialize user's diary storage
        diary_storage = DiaryStorage(self.users[username]["diary_file"])
        diary_storage.save_entries({})  # Create empty diary
        return True
    
    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        if username not in self.users:
            raise DiaryExceptions.ValidationError("Username not found!")
            
        if self.users[username]["password"] != password:
            raise DiaryExceptions.ValidationError("Incorrect password!")
            
        return True
        
    def get_user_diary_storage(self, username: str) -> DiaryStorage:
        """Get the diary storage instance for a user"""
        if username not in self.users:
            raise DiaryExceptions.ValidationError("User not found!")
            
        return DiaryStorage(self.users[username]["diary_file"])
    
    def has_users(self) -> bool:
        """Check if any users exist"""
        return len(self.users) > 0
    
    def get_usernames(self) -> List[str]:
        """Get list of all usernames"""
        return list(self.users.keys())


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


class StartupDialog:
    """Initial dialog to choose between registration and login"""
    
    def __init__(self, parent, user_storage):
        self.parent = parent
        self.user_storage = user_storage
        self.choice = None  # "register", "login", or None (cancel)
        
        # Create startup window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Personal Diary - Welcome")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self._center_window()
        
        # Create the interface
        self._create_startup_interface()
        
        # Handle window closing
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
    
    def _center_window(self):
        """Centers the dialog on screen"""
        self.dialog.transient(self.parent)
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
    
    def _create_startup_interface(self):
        """Creates the startup interface"""
        # Main container
        main_frame = ttk.Frame(self.dialog, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Welcome title
        title_label = ttk.Label(main_frame, text="Welcome to Personal Diary", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Your secure digital journal", 
                                  font=('Arial', 12))
        subtitle_label.pack(pady=(0, 30))
        
        # Check if users exist to determine which options to show
        has_users = self.user_storage.has_users()
        
        if has_users:
            # Show both options if users exist
            info_label = ttk.Label(main_frame, 
                                  text="Choose an option to continue:",
                                  font=('Arial', 11))
            info_label.pack(pady=(0, 20))
            
            # Buttons frame
            buttons_frame = ttk.Frame(main_frame)
            buttons_frame.pack(pady=10)
            
            # Login button (prominent for existing users)
            login_btn = ttk.Button(buttons_frame, text="Login to Existing Diary",
                                  command=self._choose_login,
                                  style='Accent.TButton',
                                  width=25)
            login_btn.pack(pady=(0, 10))
            
            # Register button
            register_btn = ttk.Button(buttons_frame, text="Create New Diary",
                                     command=self._choose_register,
                                     width=25)
            register_btn.pack(pady=(0, 10))
            
        else:
            # Only show registration option for first-time users
            info_label = ttk.Label(main_frame, 
                                  text="Welcome! Let's create your first diary.",
                                  font=('Arial', 11))
            info_label.pack(pady=(0, 20))
            
            # Buttons frame
            buttons_frame = ttk.Frame(main_frame)
            buttons_frame.pack(pady=10)
            
            # Only register button
            register_btn = ttk.Button(buttons_frame, text="Create New Diary",
                                     command=self._choose_register,
                                     style='Accent.TButton',
                                     width=25)
            register_btn.pack(pady=(0, 10))
        
        # Cancel/Exit button
        cancel_btn = ttk.Button(buttons_frame, text="Exit",
                               command=self._on_cancel,
                               width=25)
        cancel_btn.pack(pady=(10, 0))
    
    def _choose_register(self):
        """User chose to register"""
        self.choice = "register"
        self.dialog.destroy()
    
    def _choose_login(self):
        """User chose to login"""
        self.choice = "login"
        self.dialog.destroy()
    
    def _on_cancel(self):
        """User canceled/exited"""
        self.choice = None
        self.dialog.destroy()


class RegistrationDialog:
    """Dialog for user registration"""
    
    def __init__(self, parent, user_storage):
        self.parent = parent
        self.user_storage = user_storage
        self.success = False
        self.username = ""
        self.password = ""
        
        # Create registration window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Personal Diary - Create Account")
        self.dialog.geometry("450x400")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self._center_window()
        
        # Create the interface
        self._create_registration_interface()
        
        # Handle window closing
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
    
    def _center_window(self):
        """Centers the dialog on screen"""
        self.dialog.transient(self.parent)
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"450x400+{x}+{y}")
    
    def _create_registration_interface(self):
        """Creates the registration interface"""
        # Main container
        main_frame = ttk.Frame(self.dialog, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Create Your Diary Account", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                text="Choose a username and secure password for your diary.",
                                font=('Arial', 11),
                                wraplength=350)
        instructions.pack(pady=(0, 25))
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Username field
        ttk.Label(form_frame, text="Username:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = ttk.Entry(form_frame, font=('Arial', 12), width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Username requirements
        username_req = ttk.Label(form_frame, 
                               text="• 3-20 characters, letters and numbers only",
                               font=('Arial', 9),
                               foreground='gray')
        username_req.pack(anchor=tk.W, pady=(0, 15))
        
        # Password field
        ttk.Label(form_frame, text="Password:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = ttk.Entry(form_frame, show="*", font=('Arial', 12), width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Confirm password field
        ttk.Label(form_frame, text="Confirm Password:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.confirm_password_entry = ttk.Entry(form_frame, show="*", font=('Arial', 12), width=30)
        self.confirm_password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Password requirements
        password_req = ttk.Label(form_frame, 
                               text="• At least 6 characters\n• Mix of letters and numbers recommended",
                               font=('Arial', 9),
                               foreground='gray')
        password_req.pack(anchor=tk.W, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X)
        
        # Create account button
        create_btn = ttk.Button(buttons_frame, text="Create Account",
                               command=self._handle_registration,
                               style='Accent.TButton')
        create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = ttk.Button(buttons_frame, text="Cancel",
                               command=self._on_cancel)
        cancel_btn.pack(side=tk.LEFT)
        
        # Back to login button (if users exist)
        if self.user_storage.has_users():
            login_btn = ttk.Button(buttons_frame, text="Back to Login",
                                  command=self._back_to_login)
            login_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.confirm_password_entry.bind('<Return>', lambda e: self._handle_registration())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def _validate_input(self):
        """Validates user input"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate username
        if not username:
            raise DiaryExceptions.ValidationError("Username is required!")
        
        if len(username) < 3:
            raise DiaryExceptions.ValidationError("Username must be at least 3 characters!")
        
        if len(username) > 20:
            raise DiaryExceptions.ValidationError("Username must be 20 characters or less!")
        
        if not username.replace('_', '').isalnum():
            raise DiaryExceptions.ValidationError("Username can only contain letters, numbers, and underscores!")
        
        # Validate password
        if not password:
            raise DiaryExceptions.ValidationError("Password is required!")
        
        if len(password) < 6:
            raise DiaryExceptions.ValidationError("Password must be at least 6 characters!")
        
        if password != confirm_password:
            raise DiaryExceptions.ValidationError("Passwords don't match!")
        
        return username, password
    
    def _handle_registration(self):
        """Handles the registration process"""
        try:
            username, password = self._validate_input()
            
            # Attempt to register user
            self.user_storage.register_user(username, password)
            
            # Success
            self.username = username
            self.password = password
            self.success = True
            
            messagebox.showinfo("Success", 
                               f"Account created successfully!\nWelcome {username}!")
            
            self.dialog.destroy()
            
        except DiaryExceptions.ValidationError as e:
            messagebox.showerror("Registration Error", str(e))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {str(e)}")
    
    def _back_to_login(self):
        """Return to login without registering"""
        self.success = "back_to_login"
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Cancel registration"""
        self.success = False
        self.dialog.destroy()


class LoginDialog:
    """Updated login dialog with username selection"""
    
    def __init__(self, parent, user_storage):
        self.parent = parent
        self.user_storage = user_storage
        self.success = False
        self.username = ""
        self.password = ""
        
        # Create login window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Personal Diary - Login")
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self._center_window()
        
        # Create the interface
        self._create_login_interface()
        
        # Handle window closing
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
    
    def _center_window(self):
        """Centers the dialog on screen"""
        self.dialog.transient(self.parent)
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"400x350+{x}+{y}")
    
    def _create_login_interface(self):
        """Creates the login interface"""
        # Main container
        main_frame = ttk.Frame(self.dialog, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Welcome Back!", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 30))
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Username selection
        ttk.Label(form_frame, text="Select Username:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.username_var = tk.StringVar()
        self.username_combo = ttk.Combobox(form_frame, textvariable=self.username_var,
                                          font=('Arial', 12), width=27,
                                          state="readonly")
        
        # Populate with existing usernames
        usernames = self.user_storage.get_usernames()
        self.username_combo['values'] = usernames
        if usernames:
            self.username_combo.set(usernames[0])  # Select first user by default
        
        self.username_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        ttk.Label(form_frame, text="Password:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = ttk.Entry(form_frame, show="*", font=('Arial', 12), width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self._handle_login())
        
        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Login button
        login_btn = ttk.Button(buttons_frame, text="Login",
                              command=self._handle_login,
                              style='Accent.TButton')
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create new account button
        new_account_btn = ttk.Button(buttons_frame, text="Create New Account",
                                    command=self._create_new_account)
        new_account_btn.pack(side=tk.LEFT)
        
        # Cancel button
        cancel_btn = ttk.Button(buttons_frame, text="Cancel",
                               command=self._on_cancel)
        cancel_btn.pack(side=tk.RIGHT)
        
        # Focus on password entry
        self.password_entry.focus()
    
    def _handle_login(self):
        """Handles login attempt"""
        username = self.username_var.get().strip()
        password = self.password_entry.get()
        
        if not username:
            messagebox.showerror("Login Error", "Please select a username!")
            return
        
        if not password:
            messagebox.showerror("Login Error", "Please enter your password!")
            return
        
        try:
            # Verify credentials
            if self.user_storage.verify_user(username, password):
                # Set login details
                self.username = username  # This is critical
                self.password = password
                self.diary_lock = DiaryLock(password)
                if self.diary_lock.unlock(password):  # Verify the password with DiaryLock
                    self.success = True
                    messagebox.showinfo("Success", f"Welcome back, {username}!")
                    self.dialog.destroy()
                
        except DiaryExceptions.ValidationError as e:
            messagebox.showerror("Login Error", str(e))
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def _create_new_account(self):
        """Switch to account creation"""
        self.success = "create_account"
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Cancel login"""
        self.success = False
        self.dialog.destroy()


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
        self.frame = ttk.LabelFrame(self.parent, text="Calendar Navigation", 
                                   padding="15")
        
        # Navigation header
        nav_frame = ttk.Frame(self.frame)
        nav_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Previous month button
        self.prev_button = ttk.Button(nav_frame, text="<", width=3,
                                     command=self._navigate_previous_month)
        self.prev_button.pack(side=tk.LEFT)
        
        # Month/Year display
        self.month_year_label = ttk.Label(nav_frame, font=('Arial', 14, 'bold'))
        self.month_year_label.pack(side=tk.LEFT, expand=True)
        
        # Next month button
        self.next_button = ttk.Button(nav_frame, text=">", width=3,
                                     command=self._navigate_next_month)
        self.next_button.pack(side=tk.RIGHT)
        
        # Calendar grid container
        self.calendar_grid = ttk.Frame(self.frame)
        self.calendar_grid.pack()
        
        # Today button for quick navigation
        today_frame = ttk.Frame(self.frame)
        today_frame.pack(fill=tk.X, pady=(15, 0))
        
        today_btn = ttk.Button(today_frame, text="Go to Today", 
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
                                          width=4,
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


class DiaryMainInterface:
    """Main diary application interface with updated authentication"""
    
    def __init__(self):
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("Personal Diary Application")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Initialize storage and state
        self.user_storage = UserStorage()  # Initialize user storage first
        self.diary_storage = None  # Will be initialized after login
        self.diary = None  # Will be initialized after login
        
        # Current state variables
        self.current_date = None
        self.current_user = None
        self.is_modified = False
        self.is_saving = False
        self.diary_lock = None
        self.action_buttons = {}
        
        # Configure styles
        self._configure_styles()
        
        # Show authentication flow
        if not self._handle_authentication_flow():
            self.root.destroy()
            return
        
        # Create main interface
        self._create_main_interface()
        
        # Initialize with today's date
        self._load_date_entry(date.today())
    
    def _configure_styles(self):
        """Configures custom styles for the interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom button styles
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        style.configure('Calendar.TButton', font=('Arial', 9))
    
    def _handle_authentication_flow(self):
        """Handles the complete authentication flow"""
        while True:
            # Show startup dialog
            startup_dialog = StartupDialog(self.root, self.user_storage)
            self.root.wait_window(startup_dialog.dialog)
            
            if startup_dialog.choice is None:
                # User canceled/exited
                return False
            
            elif startup_dialog.choice == "register":
                # Show registration dialog
                registration_dialog = RegistrationDialog(self.root, self.user_storage)
                self.root.wait_window(registration_dialog.dialog)
                
                if registration_dialog.success is True:
                    # Registration successful, proceed to main app
                    self.current_user = registration_dialog.username
                    self._setup_user_session(registration_dialog.username, registration_dialog.password)
                    return True
                elif registration_dialog.success == "back_to_login":
                    # User wants to go back to login, continue loop
                    continue
                else:
                    # Registration canceled
                    return False
            
            elif startup_dialog.choice == "login":
                # Show login dialog
                while True:
                    login_dialog = LoginDialog(self.root, self.user_storage)
                    self.root.wait_window(login_dialog.dialog)
                    
                    if login_dialog.success is True:
                        # Login successful
                        self.current_user = login_dialog.username
                        self._setup_user_session(login_dialog.username, login_dialog.password)
                        return True
                    elif login_dialog.success == "create_account":
                        # User wants to create account, break to outer loop
                        break
                    else:
                        # Login canceled
                        return False
    
    def _setup_user_session(self, username, password):
        """Sets up the user session after successful authentication"""
        try:
            # Initialize diary lock
            self.diary_lock = DiaryLock(password)
            self.diary_lock.unlock(password)
            
            # Get user's diary storage and initialize diary
            self.diary_storage = self.user_storage.get_user_diary_storage(username)
            self.diary = Diary()
            self.diary.store = self.diary_storage
            
            # Set current user
            self.current_user = username
            
            # Welcome message
            messagebox.showinfo("Welcome", f"Welcome {username}!\nYour diary is ready.")
            
        except Exception as e:
            messagebox.showerror("Session Error", f"Failed to initialize session: {str(e)}")
            raise
    
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
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Diary", command=self._export_diary)
        file_menu.add_command(label="Import Entries", command=self._import_entries)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._handle_exit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy Text", command=self._copy_text,
                             accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste Text", command=self._paste_text,
                             accelerator="Ctrl+V")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Go to Today", command=self._go_to_today)
        view_menu.add_command(label="Entry Statistics", command=self._show_statistics)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Quick Tutorial", command=self._show_tutorial)
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._show_about)
    
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
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions", padding="10")
        actions_frame.pack(fill=tk.X, pady=(0, 15))
        
        buttons = [
            ("Save", self._save_current_entry),
            ("Search", self._show_search_dialog),
            ("Delete", self._delete_current_entry),
            ("Today", self._go_to_today),
            ("View All", self._view_all_entries)
        ]
        
        # Create and store button references
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(actions_frame, text=text, command=command, width=15)
            row, col = divmod(i, 2)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
            self.action_buttons[text] = btn
        
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
        
        ttk.Label(title_frame, text="Entry Title (Optional):", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        
        self.title_entry = ttk.Entry(title_frame, font=('Arial', 12))
        self.title_entry.pack(fill=tk.X, pady=(5, 0))
        self.title_entry.bind('<KeyRelease>', self._on_content_modified)
        
        # Content editor section
        editor_frame = ttk.LabelFrame(parent, text="Diary Content", padding="10")
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
        
        # Load the selected date
        self._load_date_entry(selected_date)
    
    def _load_date_entry(self, entry_date):
        """Loads diary entry for the specified date"""
        try:
            self.current_date = entry_date
            
            # Update date display
            formatted_date = entry_date.strftime("%A, %B %d, %Y")
            self.date_display.config(text=f"Date: {formatted_date}")
            
            # Load entry data using the Diary class
            date_key = entry_date.strftime("%Y-%m-%d")
            entries = self.diary.search_by_date(date_key)
            
            if entries and entries[0]:  # If entry exists
                entry = entries[0]
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, entry['title'])
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, entry['content'])
                self.status_label.config(text=f"Loaded entry from {formatted_date}")
            else:
                # Clear for new entry
                self.title_entry.delete(0, tk.END)
                self.text_editor.delete(1.0, tk.END)
                self.status_label.config(text=f"New entry for {formatted_date}")
            
            # Reset modification flag
            self.is_modified = False
            self._update_word_count()
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load entry: {str(e)}")
    
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
    
    def _save_current_entry(self):
        """Saves the current diary entry"""
        try:
            if self.is_saving:
                messagebox.showinfo("Please Wait", "Save operation in progress...")
                return
                
            if not self.current_date:
                messagebox.showwarning("No Date Selected", "Please select a date first!")
                return
                
            self.is_saving = True
            
            # Get current content
            title = self.title_entry.get().strip()
            content = self.text_editor.get(1.0, tk.END).strip()
            
            if not content and not title:
                messagebox.showinfo("Nothing to Save", "Entry is empty!")
                return
            
            # Prepare entry data
            date_key = self.current_date.strftime("%Y-%m-%d")
            new_entry = {
                "title": title,
                "content": content,
                "date": date_key
            }
            
            # Save entry using diary class
            self.diary.create_entry(new_entry)
            
            # Update UI
            self.is_modified = False
            formatted_date = self.current_date.strftime("%B %d, %Y")
            self.status_label.config(text=f"Entry saved for {formatted_date}")
            
            messagebox.showinfo("Save Successful", f"Entry saved for {formatted_date}!")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save entry: {str(e)}")
        finally:
            self.is_saving = False
    
    def _delete_current_entry(self):
        """Deletes the current diary entry"""
        try:
            if not self.current_date:
                messagebox.showwarning("No Date Selected", "Please select a date first!")
                return
            
            date_key = self.current_date.strftime("%Y-%m-%d")
            entries = self.diary.search_by_date(date_key)
            
            if not entries or not entries[0]:
                messagebox.showinfo("No Entry", "No entry exists for this date!")
                return
            
            # Confirm deletion
            formatted_date = self.current_date.strftime("%B %d, %Y")
            result = messagebox.askyesno("Confirm Deletion", 
                                       f"Are you sure you want to delete the entry for {formatted_date}?")
            
            if result:
                self.diary.delete_entry(date_key)
                self.title_entry.delete(0, tk.END)
                self.text_editor.delete(1.0, tk.END)
                self.is_modified = False
                self.status_label.config(text=f"Entry deleted for {formatted_date}")
                messagebox.showinfo("Delete Successful", f"Entry deleted for {formatted_date}!")
                
        except Exception as e:
            messagebox.showerror("Delete Error", f"Failed to delete entry: {str(e)}")
    
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
        """Shows search dialog - placeholder"""
        messagebox.showinfo("Search", "Search functionality would be implemented here")
    
    def _view_all_entries(self):
        """View all entries - placeholder"""
        messagebox.showinfo("View All", "View all entries functionality would be implemented here")
    
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
        """Export diary functionality"""
        messagebox.showinfo("Export", "Export functionality would save your diary to a file!")
    
    def _import_entries(self):
        """Import entries functionality"""
        messagebox.showinfo("Import", "Import functionality would load entries from a file!")
    
    def _show_statistics(self):
        """Shows diary statistics"""
        try:
            entries = self.diary_storage.list_entries()
            total_entries = len(entries)
            total_words = sum(len(entry.get('content', '').split()) for entry in entries.values())
            
            stats_msg = f"""Diary Statistics:
        
Total Entries: {total_entries}
Total Words: {total_words}
Average Words per Entry: {total_words // max(total_entries, 1)}
Date Range: {len(entries)} days with entries"""
            
            messagebox.showinfo("Diary Statistics", stats_msg)
        except Exception as e:
            messagebox.showerror("Statistics Error", f"Failed to calculate statistics: {str(e)}")
    
    def _show_tutorial(self):
        """Shows quick tutorial"""
        tutorial_msg = """Quick Tutorial:
        
1. Click on calendar dates to navigate
2. Type your diary entry in the text area
3. Add an optional title
4. Press Ctrl+S or click Save to save
5. Use the quick action buttons for common tasks
        
Tip: The app will remind you to save unsaved changes!"""
        
        messagebox.showinfo("Quick Tutorial", tutorial_msg)
    
    def _show_shortcuts(self):
        """Shows keyboard shortcuts"""
        shortcuts_msg = """Keyboard Shortcuts:
        
Ctrl+S - Save current entry
Ctrl+F - Search entries  
Ctrl+C - Copy selected text
Ctrl+V - Paste text
Ctrl+N - Clear current entry
Del - Delete current entry
Ctrl+A - Select all text"""
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_msg)
    
    def _show_about(self):
        """Shows about dialog"""
        about_msg = f"""Personal Diary Application
        
Version: 2.0 (Multi-User)
User: {self.current_user}
Created with: Python & Tkinter
        
Features:
- Multi-user support with secure login
- Intuitive calendar navigation
- Rich text editing
- Entry management
- Clean, modern interface
- Keyboard shortcuts

Your personal diary with secure user authentication."""
        
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
        
        messagebox.showinfo("Goodbye", f"Thank you for using Personal Diary, {self.current_user}!")
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
# --- END OF FILE ---
