from src.income import update_income

result = update_income(
    income_id=6,
    user_id=1,
    amount=35000
)

print("Updated rows:", result)