from src.summary import get_yearly_summary

total = get_yearly_summary(
    user_id=1,
    start_date="2026-01-01",
    end_date="2026-12-31"
)

print("This year's spending:", total)