
import sqlite3
from tkinter import messagebox

class DbHandler:
    def __init__(self):
        try:
            self.connect_db()
            self.create_user_table()
            self.create_image_table()
        except sqlite3.Error as e:
            self.show_error(f"Database error: {e}")

    def connect_db(self):
        try:
            self.connection = sqlite3.connect('CryptoCanvas.db')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            self.show_error(f"Database connection error: {e}")

    def create_user_table(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users "
                                "(id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, salt BLOB)")
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error creating user table: {e}")

    def create_image_table(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS images "
                                "(id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, data BLOB, "
                                "UNIQUE(user_id, name))")
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error creating image table: {e}")

    def get_images_by_user_id(self, user_id, limit=10, offset=0):
        try:
            self.cursor.execute("SELECT name FROM images WHERE user_id = ? LIMIT ? OFFSET ?",
                                (user_id, limit, offset))
            rows = self.cursor.fetchmany(limit)
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            self.show_error(f"Error creating image table: {e}")

    def get_image_by_name(self, user_id, name):
        try:
            self.cursor.execute("SELECT * FROM images WHERE user_id = ? AND name = ?",
                (user_id, name))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            self.show_error(f"Error fetching image: {e}")

    def get_user(self, email):
        try:
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            self.show_error(f"Error fetching user: {e}")

    def add_image(self, user_id, name, image_data):
        try:
            self.cursor.execute(
                "INSERT INTO images (user_id, name, data) VALUES (?, ?, ?)",
                (user_id, name, image_data))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            self.show_error(f'Operation failed. Image name ({name}) must be unique.')
            raise e
        except sqlite3.Error as e:
            self.show_error(f"Error adding image: {type(e).__name__}: {e}")

    def delete_image(self, user_id, name):
        try:
            self.cursor.execute(
                "DELETE FROM images WHERE user_id = ? AND name = ?",
                (user_id, name))
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error deleting image: {e}")

    def add_user(self, name, email, password, salt):
        try:
            self.cursor.execute(
                "INSERT INTO users (name, email, password, salt) VALUES (?, ?, ?, ?)",
                (name, email, password, salt))
            self.connection.commit()
        except sqlite3.Error as e:
            self.show_error(f"Error adding user: {e}")

    def disconnect_db(self):
        self.connection.close()

    def show_error(self, msg):
        messagebox.showerror('Error', msg)
