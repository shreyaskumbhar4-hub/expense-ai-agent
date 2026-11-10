from src.ai import understand_expense
from src.expense import add_expense


user_id = 1

text = "I spent 500 rupees on food today."

expense = understand_expense(text)

print("AI extracted:", expense)

add_expense(
    user_id=user_id,
    amount=expense["amount"],
    category=expense["category"],
    expense_date=expense["date"]
)

print("Expense added successfully.")