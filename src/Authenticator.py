from argon2 import PasswordHasher
from re import match
from tkinter import simpledialog, messagebox
from DbHandler import DbHandler

class Authenticator:
    """Handles user authentication operations."""

    def __init__(self):
        """Initialize the Authenticator."""
        self.logged_in = False
        self.current_user = None
        self.db_handler = DbHandler()
        self.password_hasher = PasswordHasher(time_cost=1, memory_cost=47104, parallelism=1) # https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#argon2id

    def hash_password(self, password):
        """Hashes the given password using Argon2.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        hashed_password = self.password_hasher.hash(password)
        return hashed_password

    def verify_password(self, hashed_password, password):
        """Verifies if the given password matches the hashed password.

        Args:
            hashed_password (str): The hashed password.
            password (str): The password to verify.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        try:
            self.password_hasher.verify(hashed_password, password)
            return True
        except:
            return False

    def sign_up(self):
        """Registers a new user."""
        email = ''
        email_validate_pattern = r"^\S+@\S+\.\S+$" # https://uibakery.io/regex-library/email-regex-python
        self.db_handler.connect_db()
        existing_user = self.db_handler.get_user(email)
        while not match(email_validate_pattern, email):
            email = simpledialog.askstring('Email', 'Enter email:')
            if not email:
                messagebox.showerror('Error', 'Operation canceled.')
                return
            if existing_user:
                messagebox.showerror('Error', 'User with this email already exists.')
            elif not match(email_validate_pattern, email):
                messagebox.showerror('Error', 'Invalid email format.')
        password = ''
        password_validate_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"  # https://www.geeksforgeeks.org/password-validation-in-python/
        while not match(password_validate_pattern, password):
            password = simpledialog.askstring('Password', 'Enter password:', show='*')
            if not password:
                messagebox.showerror('Error', 'Operation canceled.')
                return
            if not match(password_validate_pattern, password):
                messagebox.showerror('Error', 'Invalid password format.\n'
                                              'The password requires:\n'
                                              '1. a number.\n'
                                              '2. an uppercase letter.\n'
                                              '3. a lowercase character.\n'
                                              '4. a special symbol.\n'
                                              '5. length of 6 to 20 characters.')
        hashed_password = self.hash_password(password)
        name = simpledialog.askstring('Name', 'Enter name:')
        if not name:
            messagebox.showerror('Error', 'Operation canceled.')
            return
        self.db_handler.add_user(name, email, hashed_password)
        self.logged_in = True
        user_id = self.db_handler.get_user(email)[0]
        self.current_user = CurrentUser(user_id, name)
        messagebox.showinfo('Success', f'Signed up successfully as {self.current_user.name}')

    def sign_in(self):
        """Signs in a user."""
        user = None
        self.db_handler.connect_db()
        while not user:
            email = simpledialog.askstring('Email', 'Enter email:')
            if not email:
                messagebox.showerror('Error', 'Operation canceled.')
                return
            user = self.db_handler.get_user(email)
            if not user:
                messagebox.showerror('Error', 'User not found.')
        user_id, name, stored_email, stored_password = user
        attempts = 3
        while attempts > 0:
            password = simpledialog.askstring('Password', 'Enter password:', show='*')
            if not password:
                messagebox.showerror('Error', 'Operation canceled.')
                return
            if self.password_hasher.verify(stored_password, password):
                if self.password_hasher.check_needs_rehash(stored_password):
                    new_hash = self.hash_password(password)
                    self.db_handler.update_user_password(user_id, new_hash)
                self.logged_in = True
                self.current_user = CurrentUser(user_id, name)
                messagebox.showinfo('Success',
                                    f'Signed in successfully as {self.current_user.name}')
                return
            else:
                messagebox.showwarning('Warning', 'Incorrect password.')
                attempts -= 1
        messagebox.showerror('Error', 'Maximum login attempts exceeded.')

    def sign_out(self):
        """Signs out the current user."""
        self.db_handler.disconnect_db()
        self.logged_in = False
        name = self.current_user.name
        self.current_user = None
        messagebox.showinfo('Success', f'Signed out successfully as {name}')


class CurrentUser:
    """Represents the currently logged-in user."""

    def __init__(self, user_id, name):
        """Initialize the CurrentUser instance.

        Args:
            user_id (int): The ID of the user.
            name (str): The name of the user.
        """
        self.id = user_id
        self.name = name
