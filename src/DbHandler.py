import sqlite3
from tkinter import messagebox

class DbHandler:
    """Handles database operations for CryptoCanvas application."""

    def __init__(self):
        """Initialize the DbHandler by connecting to the database and creating necessary tables."""
        try:
            self.connect_db()
            self.create_user_table()
            self.create_image_table()
        except sqlite3.Error as e:
            self.show_error(f"Database error: {e}")

    def connect_db(self):
        """Connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect('CryptoCanvas.db')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            self.show_error(f"Database connection error: {e}")

    def create_user_table(self):
        """Create the user table in the database if it does not exist."""
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users "
                                "(id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT)")
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error creating user table: {e}")

    def create_image_table(self):
        """Create the image table in the database if it does not exist."""
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS images "
                                "(id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, data BLOB, "
                                "UNIQUE(user_id, name))")
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error creating image table: {e}")

    def get_images_by_user_id(self, user_id, limit=10, offset=0):
        """Retrieve image names associated with a user from the database."""
        try:
            self.cursor.execute("SELECT name FROM images WHERE user_id = ? LIMIT ? OFFSET ?",
                                (user_id, limit, offset))
            rows = self.cursor.fetchmany(limit)
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            self.show_error(f"Error fetching images by user ID: {e}")

    def get_image_by_name(self, user_id, name):
        """Retrieve image data by user ID and image name from the database."""
        try:
            self.cursor.execute("SELECT * FROM images WHERE user_id = ? AND name = ?",
                                (user_id, name))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            self.show_error(f"Error fetching image by name: {e}")

    def get_user(self, email):
        """Retrieve user information by email from the database."""
        try:
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            self.show_error(f"Error fetching user by email: {e}")

    def add_image(self, user_id, name, image_data):
        """Add an image to the database."""
        try:
            self.cursor.execute(
                "INSERT INTO images (user_id, name, data) VALUES (?, ?, ?)",
                (user_id, name, image_data))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            self.show_error(f'Operation failed. Image name ({name}) must be unique.')
            raise e
        except sqlite3.Error as e:
            self.show_error(f"Error adding image: {e}")

    def delete_image(self, user_id, name):
        """Delete an image from the database."""
        try:
            self.cursor.execute(
                "DELETE FROM images WHERE user_id = ? AND name = ?",
                (user_id, name))
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error deleting image: {e}")

    def add_user(self, name, email, password):
        """Add a user to the database."""
        try:
            self.cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password))
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error adding user: {e}")

    def update_user_password(self, user_id, new_password):
        """Update the password for a user in the database."""
        try:
            self.cursor.execute("UPDATE users SET password = ? WHERE id = ?",
                (new_password, user_id))
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error updating password: {e}")

    def disconnect_db(self):
        """Close the database connection."""
        self.connection.close()

    def show_error(self, msg):
        """Display an error message dialog."""
        messagebox.showerror('Error', msg)
