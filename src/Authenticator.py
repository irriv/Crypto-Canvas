
import hashlib
import os
import re
from tkinter import simpledialog, messagebox

from DbHandler import DbHandler

class Authenticator:
    def __init__(self):
        self.logged_in = False
        self.current_user = None
        self.db_handler = DbHandler()

    def hash_password(self, password, salt):
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return hashed_password

    def sign_up(self):
        if not self.logged_in:
            email = simpledialog.askstring('Email', 'Enter email:')
            self.db_handler.connect_db()
            existing_user = self.db_handler.get_user(email)
            if existing_user:
                messagebox.showerror('Error', 'User with this email already exists.')
                return
            # email_validate_pattern = r"^\S+@\S+\.\S+$"
            # re.match(email_validate_pattern, email)
            password = simpledialog.askstring('Password', 'Enter password:')
            # password_validate_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            # re.match(password_validate_pattern, password)
            salt = os.urandom(32)
            hashed_password = self.hash_password(password, salt)
            name = simpledialog.askstring('Name', 'Enter name:')
            # Insert the user into the database with hashed password and salt
            self.db_handler.add_user(name, email, hashed_password, salt)
            self.logged_in = True
            user_id = self.db_handler.get_user(email)[0]
            self.current_user = CurrentUser(user_id, name)
            messagebox.showinfo('Success', f'Signed up successfully as {self.current_user.name}')

    def sign_in(self):
        if not self.logged_in:
            email = simpledialog.askstring('Email', 'Enter email:')
            password = simpledialog.askstring('Password',
                                              'Enter password:')
            self.db_handler.connect_db()
            user = self.db_handler.get_user(email)
            if user:
                user_id, name, stored_email, stored_password, salt = user
                hashed_password = self.hash_password(password, salt)
                if hashed_password == stored_password:
                    self.logged_in = True
                    self.current_user = CurrentUser(user_id, name)
                    messagebox.showinfo('Success',
                                        f'Signed in successfully as {self.current_user.name}')
                else:
                    messagebox.showwarning('Warning',
                                           'Incorrect password.')
            else:
                messagebox.showerror('Error', 'User not found.')

    def sign_out(self):
        if self.logged_in:
            self.db_handler.disconnect_db()
            self.logged_in = False
            messagebox.showinfo('Success', f'Signed out successfully as {self.current_user.name}')
            self.current_user = None


class CurrentUser:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
