import sqlite3
from datetime import datetime


def add_expense(
    user_id,
    amount,
    category,
    expense_date,
    expense_time=None,
    notes=None,
    status="confirmed"
):

    connection = sqlite3.connect("database/expense_tracker.db")

    now = datetime.now().isoformat()

    connection.execute("""
    INSERT INTO expenses (
        user_id,
        amount,
        category,
        expense_date,
        expense_time,
        notes,
        status,
        created_at,
        updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        amount,
        category,
        expense_date,
        expense_time,
        notes,
        status,
        now,
        now
    ))
    connection.commit()
def get_expenses(user_id):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    SELECT *
    FROM expenses
    WHERE user_id = ?
    ORDER BY expense_date DESC
    """, (user_id,))

    rows = cursor.fetchall()
    connection.close()
    return rows
def delete_expense(expense_id, user_id):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    DELETE FROM expenses
    WHERE id = ?
      AND user_id = ?
    """, (expense_id, user_id))

    connection.commit()

    deleted_rows = cursor.rowcount

    connection.close()

    return deleted_rows

def update_expense(expense_id, user_id, amount):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    UPDATE expenses
    SET amount = ?,
        updated_at = ?
    WHERE id = ?
      AND user_id = ?
    """, (
        amount,
        datetime.now().isoformat(),
        expense_id,
        user_id
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows




    