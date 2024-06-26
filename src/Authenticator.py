from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
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
        """Hashes the given password using Argon2id.

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

    def check_needs_rehash(self, hashed_password):
        """Check if the hashed password needs rehashing.

            Args:
                hashed_password (str): The hashed password to check.

            Returns:
                bool: True if the hashed password needs rehashing, False otherwise.
            """
        return self.password_hasher.check_needs_rehash(hashed_password)

    def sign_up(self):
        """Registers a new user."""
        email = ''
        email_validate_pattern = r"^\S+@\S+\.\S+$" # https://uibakery.io/regex-library/email-regex-python
        self.db_handler.connect_db()
        while not match(email_validate_pattern, email):
            email = simpledialog.askstring('Email', 'Enter email:')
            if not email:
                messagebox.showerror('Error', 'Operation canceled.')
                return
            existing_user = self.db_handler.get_user(email)
            if existing_user:
                messagebox.showerror('Error', 'User with this email already exists.')
                email = ''
            elif not match(email_validate_pattern, email):
                messagebox.showerror('Error', 'Invalid email format.')
        password = ''
        password_validate_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$"
        while not match(password_validate_pattern, password):
            password = simpledialog.askstring('Password', 'Enter password:', show='*')
            if not password:
                messagebox.showerror('Error', 'Operation canceled.')
                return
            if not match(password_validate_pattern, password):
                messagebox.showerror('Error', 'Invalid password format.\n'
                                              'The password requires:\n'
                                              '1. an uppercase letter.\n'
                                              '2. a lowercase character.\n'
                                              '3. a number.\n'
                                              '4. length of 8 characters or greater.')
        name = simpledialog.askstring('Name', 'Enter name:')
        if not name:
            messagebox.showerror('Error', 'Operation canceled.')
            return
        hashed_password = self.hash_password(password)
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
            try:
                if self.verify_password(stored_password, password):
                    if self.check_needs_rehash(stored_password):
                        new_hash = self.hash_password(password)
                        self.db_handler.update_user_password(user_id, new_hash)
                    self.logged_in = True
                    self.current_user = CurrentUser(user_id, name)
                    messagebox.showinfo('Success',
                                        f'Signed in successfully as {self.current_user.name}')
                    return
                else:
                    attempts -= 1
                    messagebox.showwarning('Warning', 'Incorrect password.')
            except VerifyMismatchError as e:
                attempts -= 1
                messagebox.showwarning('Warning', 'Incorrect password.')
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
