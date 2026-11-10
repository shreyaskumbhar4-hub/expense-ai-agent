from src.summary import get_monthly_summary

total = get_monthly_summary(
    user_id=1,
    start_date="2026-10-01",
    end_date="2026-10-31"
)

print("This month's spending:", total)


