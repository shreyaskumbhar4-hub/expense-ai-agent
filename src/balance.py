import sqlite3


def get_balance(user_id):
    connection = sqlite3.connect("database/expense_tracker.db")

    income_cursor = connection.execute("""
    SELECT COALESCE(SUM(amount), 0)
    FROM income
    WHERE user_id = ?
      AND status = 'confirmed'
    """, (user_id,))

    total_income = income_cursor.fetchone()[0]

    expense_cursor = connection.execute("""
    SELECT COALESCE(SUM(amount), 0)
    FROM expenses
    WHERE user_id = ?
      AND status = 'confirmed'
    """, (user_id,))

    total_expenses = expense_cursor.fetchone()[0]

    connection.close()

    return total_income - total_expenses