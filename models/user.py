import sqlite3
from database import get_db_connection



class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    @staticmethod
    def register(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return "User registered successfully!"
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()

    @staticmethod
    def login(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return User(user[0], username)
        else:
            return None

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()



def update_avatar(user_id, avatar_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET avatar_path = ? WHERE user_id = ?", (avatar_path, user_id))
    conn.commit()
    conn.close()

def get_avatar(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT avatar_path FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ''