import sqlite3

connection = sqlite3.connect("database/expense_tracker.db")

connection.execute("""
DELETE FROM income
WHERE id IN (10, 14)
AND user_id = 1
""")

connection.commit()
connection.close()

print("Test income cleaned")