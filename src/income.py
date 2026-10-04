import sqlite3
from datetime import datetime


def add_income(
    user_id,
    amount,
    source,
    income_date,
    income_time=None,
    notes=None,
    status="confirmed"
):
    connection = sqlite3.connect("database/expense_tracker.db")

    now = datetime.now().isoformat()

    connection.execute("""
    INSERT INTO income (
        user_id,
        amount,
        source,
        income_date,
        income_time,
        notes,
        status,
        created_at,
        updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        amount,
        source,
        income_date,
        income_time,
        notes,
        status,
        now,
        now
    ))

    connection.commit()
    connection.close()


def get_income(user_id):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    SELECT *
    FROM income
    WHERE user_id = ?
    ORDER BY income_date DESC
    """, (user_id,))

    rows = cursor.fetchall()

    connection.close()

    return rows


def update_income(income_id, user_id, amount):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    UPDATE income
    SET amount = ?,
        updated_at = ?
    WHERE id = ?
      AND user_id = ?
    """, (
        amount,
        datetime.now().isoformat(),
        income_id,
        user_id
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows


def delete_income(income_id, user_id):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    DELETE FROM income
    WHERE id = ?
      AND user_id = ?
    """, (income_id, user_id))

    connection.commit()

    deleted_rows = cursor.rowcount

    connection.close()

    return deleted_rows