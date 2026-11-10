from src.user import add_user, get_user


user_id = add_user(
    name="Sam",
    currency="INR",
    timezone="Asia/Kolkata",
    week_start_on="Monday"
)

print("Created user:", user_id)

user = get_user(user_id)

print("User:", user)