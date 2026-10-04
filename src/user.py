import sqlite3
from datetime import datetime


def add_user(
    name,
    currency,
    timezone,
    week_start_on
):
    connection = sqlite3.connect("database/expense_tracker.db")

    created_at = datetime.now().isoformat()

    cursor = connection.execute("""
    INSERT INTO users (
        name,
        currency,
        timezone,
        week_start_on,
        created_at
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        currency,
        timezone,
        week_start_on,
        created_at
    ))

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user(user_id):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    SELECT *
    FROM users
    WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user