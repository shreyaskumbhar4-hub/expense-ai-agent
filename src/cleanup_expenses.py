import sqlite3

connection = sqlite3.connect("database/expense_tracker.db")

connection.execute("""
DELETE FROM expenses
WHERE id IN (2, 3,4)
""")

connection.commit()
connection.close()

print("Test expenses deleted")