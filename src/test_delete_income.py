from src.income import delete_income

result = delete_income(
    income_id=15,
    user_id=1
)

print("Deleted rows:", result)