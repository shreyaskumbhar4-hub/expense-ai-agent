from src.summary import get_daily_summary

total = get_daily_summary(
    user_id=1,
    date="2026-10-04"
)

print("Today's spending:", total)