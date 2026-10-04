
from src.summary import get_weekly_summary

total = get_weekly_summary(
    user_id=1,
    start_date="2026-09-28",
    end_date="2026-10-04"
)

print("This week's spending:", total)
