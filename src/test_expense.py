from src.expense import add_expense

add_expense(
    user_id=1,
    amount=250,
    category="Food",
    expense_date="2026-10-04"
)

print("Expense added successfully")