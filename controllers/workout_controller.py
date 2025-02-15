import sqlite3
from database import get_db_connection


def mark_workout_done(workout_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE workouts SET status = 'Done' WHERE workout_id = ?", (workout_id,))
    conn.commit()
    conn.close()


def mark_workout_pending(workout_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE workouts SET status = 'Pending' WHERE workout_id = ?", (workout_id,))
    conn.commit()
    conn.close()


def delete_workout(workout_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM workouts WHERE workout_id = ?", (workout_id,))
    conn.commit()
    conn.close()


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

def add_workout(user_id, workout_type, duration, difficulty, notes=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workouts (user_id, type, duration, difficulty, status, date, notes) VALUES (?, ?, ?, ?, 'Pending', CURRENT_DATE, ?)",
                   (user_id, workout_type, duration, difficulty, notes))
    conn.commit()
    conn.close()


def list_workouts(user_id, only_done=False, date_filter=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT workout_id, type, duration, difficulty, status, date, notes FROM workouts WHERE user_id = ?"
    params = [user_id]

    if only_done:
        query += " AND status = 'Done'"
    if date_filter:
        query += " AND date = ?"
        params.append(date_filter)

    cursor.execute(query, tuple(params))
    workouts = cursor.fetchall()
    conn.close()
    return workouts


def update_workout(workout_id, workout_type, duration, difficulty):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE workouts SET type = ?, duration = ?, difficulty = ? WHERE workout_id = ?",
        (workout_type, duration, difficulty, workout_id)
    )

    conn.commit()
    conn.close()
