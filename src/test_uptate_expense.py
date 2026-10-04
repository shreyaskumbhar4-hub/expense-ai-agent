from src.expense import update_expense

result = update_expense(
    expense_id=6,
    user_id=1,
    amount=300
)

print("Updated rows:", result)