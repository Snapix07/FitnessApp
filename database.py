import sqlite3

def get_db_connection():
    conn = sqlite3.connect("fitness_app.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT NOT NULL,
            duration INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully!")