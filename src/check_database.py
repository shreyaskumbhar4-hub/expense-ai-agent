import sqlite3

connection = sqlite3.connect("database/expense_tracker.db")

cursor = connection.execute("SELECT * FROM expenses")

rows = cursor.fetchall()

print(rows)

connection.close()