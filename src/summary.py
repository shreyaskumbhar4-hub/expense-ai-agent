import sqlite3


def get_daily_summary(user_id, date):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    SELECT COALESCE(SUM(amount), 0)
    FROM expenses
    WHERE user_id = ?
      AND expense_date = ?
      AND status = 'confirmed'
    """, (user_id, date))

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_weekly_summary(user_id, start_date, end_date):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    SELECT COALESCE(SUM(amount), 0)
    FROM expenses
    WHERE user_id = ?
      AND expense_date BETWEEN ? AND ?
      AND status = 'confirmed'
    """, (user_id, start_date, end_date))

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_monthly_summary(user_id, start_date, end_date):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    SELECT COALESCE(SUM(amount), 0)
    FROM expenses
    WHERE user_id = ?
      AND expense_date BETWEEN ? AND ?
      AND status = 'confirmed'
    """, (user_id, start_date, end_date))

    total = cursor.fetchone()[0]

    connection.close()

    return total

def get_yearly_summary(user_id, start_date, end_date):
    connection = sqlite3.connect("database/expense_tracker.db")

    cursor = connection.execute("""
    SELECT COALESCE(SUM(amount), 0)
    FROM expenses
    WHERE user_id = ?
      AND expense_date BETWEEN ? AND ?
      AND status = 'confirmed'
    """, (user_id, start_date, end_date))

    total = cursor.fetchone()[0]

    connection.close()

    return total