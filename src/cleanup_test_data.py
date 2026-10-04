import sqlite3

connection = sqlite3.connect("database/expense_tracker.db")

connection.execute("DELETE FROM income")
connection.execute("DELETE FROM expenses")

connection.commit()
connection.close()

print("Test data cleaned")