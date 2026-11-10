from src.expense import delete_expense

result = delete_expense(
    expense_id=5,
    user_id=1
)

print("Deleted rows:", result)