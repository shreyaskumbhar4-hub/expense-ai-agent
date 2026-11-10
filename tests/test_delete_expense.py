from src.expense import delete_expense
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

result = delete_expense(
    expense_id=5,
    user_id=1
)

print("Deleted rows:", result)