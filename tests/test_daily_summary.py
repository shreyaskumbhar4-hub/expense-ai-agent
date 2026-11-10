from src.summary import get_daily_summary
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

total = get_daily_summary(
    user_id=1,
    date="2026-10-04"
)

print("Today's spending:", total)