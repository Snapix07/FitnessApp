import sqlite3
from database import get_db_connection

def add_workout(user_id, workout_type, duration, difficulty):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workouts (user_id, type, duration, difficulty) VALUES (?, ?, ?, ?)",
                   (user_id, workout_type, duration, difficulty))
    conn.commit()
    conn.close()

def list_workouts(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, duration, difficulty FROM workouts WHERE user_id = ?", (user_id,))
    workouts = cursor.fetchall()
    conn.close()
    return [f"{w[0]}: {w[1]} min, {w[2]}" for w in workouts]


def mark_workout_done(workout_id):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE workouts SET status = 'Done' WHERE workout_id = ?", (workout_id,))
    conn.commit()
    conn.close()
    print(f"Workout {workout_id} marked as Done!")


def list_workouts(user_id, only_done=False):

    conn = get_db_connection()
    cursor = conn.cursor()

    if only_done:
        cursor.execute(
            "SELECT workout_id, type, duration, difficulty, status FROM workouts WHERE user_id = ? AND status = 'Done'",
            (user_id,))
    else:
        cursor.execute("SELECT workout_id, type, duration, difficulty, status FROM workouts WHERE user_id = ?",
                       (user_id,))

    workouts = cursor.fetchall()
    conn.close()
    return workouts
