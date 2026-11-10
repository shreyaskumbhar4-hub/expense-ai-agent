import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
from src.database import init_db
from src.analytics import get_category_spending

# Initialize the database and ensure tables exist
init_db()

conn = sqlite3.connect("database/expense_tracker.db")
cursor = conn.cursor()

# Clear previous test data to keep it clean
cursor.execute("DELETE FROM expenses WHERE user_id = 1")

# Insert test expenses
cursor.execute(
    "INSERT INTO expenses (user_id, amount, category, expense_date, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (1, 150.0, "Food", "2026-11-10", "confirmed", "2026-11-10T00:00:00", "2026-11-10T00:00:00")
)
cursor.execute(
    "INSERT INTO expenses (user_id, amount, category, expense_date, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (1, 50.0, "Food", "2026-11-10", "confirmed", "2026-11-10T00:00:00", "2026-11-10T00:00:00")
)
cursor.execute(
    "INSERT INTO expenses (user_id, amount, category, expense_date, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (1, 200.0, "Transport", "2026-11-10", "confirmed", "2026-11-10T00:00:00", "2026-11-10T00:00:00")
)

conn.commit()
conn.close()

print("Running analytics test...")

# Test category spending function
result = get_category_spending(user_id=1)
print("Category Spending Result:", result)

# Simple validation assertions
breakdown = result["breakdown"]
food_total = next((item["total"] for item in breakdown if item["category"] == "Food"), 0)
transport_total = next((item["total"] for item in breakdown if item["category"] == "Transport"), 0)

assert food_total == 200.0, f"Expected Food total to be 200.0, got {food_total}"
assert transport_total == 200.0, f"Expected Transport total to be 200.0, got {transport_total}"

print("Analytics test passed successfully!")