from src.income import delete_income
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

result = delete_income(
    income_id=15,
    user_id=1
)

print("Deleted rows:", result)