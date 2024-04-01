
import sqlite3

class DbHandler:
    def __init__(self):
        self.connect_db()
        self.create_user_table()
        self.create_image_table()

    def connect_db(self):
        self.connection = sqlite3.connect('CryptoCanvas.db')
        self.cursor = self.connection.cursor()

    def create_user_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users "
                            "(id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, salt BLOB)")
        self.connection.commit()

    def create_image_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS images "
                            "(id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, data BLOB, "
                            "UNIQUE(user_id, name))")
        self.connection.commit()

    def get_images_by_user_id(self, user_id, limit=10, offset=0):
        self.cursor.execute("SELECT name FROM images WHERE user_id = ? LIMIT ? OFFSET ?",
                            (user_id, limit, offset))
        rows = self.cursor.fetchmany(limit)
        return [row[0] for row in rows]

    def get_image_by_name(self, user_id, name):
        self.cursor.execute("SELECT * FROM images WHERE user_id = ? AND name = ?",
            (user_id, name))
        return self.cursor.fetchone()

    def get_user(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    def add_image(self, user_id, name, image_data):
        self.cursor.execute(
            "INSERT INTO images (user_id, name, data) VALUES (?, ?, ?)",
            (user_id, name, image_data))
        self.connection.commit()

    def delete_image(self, user_id, name):
        self.cursor.execute(
            "DELETE FROM images WHERE user_id = ? AND name = ?",
            (user_id, name))
        self.connection.commit()

    def add_user(self, name, email, password, salt):
        self.cursor.execute(
            "INSERT INTO users (name, email, password, salt) VALUES (?, ?, ?, ?)",
            (name, email, password, salt))
        self.connection.commit()

    def disconnect_db(self):
        self.connection.close()
