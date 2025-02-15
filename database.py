import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            avatar_path TEXT DEFAULT ''
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            duration INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            date TEXT DEFAULT CURRENT_DATE,
            notes TEXT DEFAULT ''
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()


def get_db_connection():
    return sqlite3.connect(DB_PATH)