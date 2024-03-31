
import sqlite3

class DbHandler:
    def __init__(self):
        self.connect_db()
        self.create_user_table()

    def connect_db(self):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

    def create_user_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users "
                            "(id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT, salt BLOB)")
        self.connection.commit()

    def search_user(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    def add_user(self, name, email, password, salt):
        self.cursor.execute(
            "INSERT INTO users (name, email, password, salt) VALUES (?, ?, ?, ?)",
            (name, email, password, salt))
        self.connection.commit()

    def disconnect_db(self):
        self.connection.close()
