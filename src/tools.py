

from src.expense import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense
)

from src.income import (
    add_income,
    get_income,
    update_income,
    delete_income
)

from src.balance import get_balance

from src.summary import (
    get_daily_summary,
    get_weekly_summary,
    get_monthly_summary,
    get_yearly_summary
)

from src.gamification import get_user_gamification_stats

def check_user_level_and_points(user_id: int):
    """
    Checks the user's current points, level, and points needed for the next level.
    """
    stats = get_user_gamification_stats(user_id)
    return (
        f"You are currently at Level {stats['level']} with {stats['points']} points! "
        f"You need {stats['points_to_next_level']} more points to reach the next level."
    )

from src.budget import (
    set_budget, 
    get_budget_status
)

from src.analytics import get_category_spending

from src.insights import get_spending_insights

from src.gamification import add_points, get_user_gamification_stats

# Example inside your expense-adding tool logic:
# After successfully inserting the expense into the database:
# user_id = 1
# points_result = add_points(user_id, points_to_add=10)



TOOLS = {
    "add_expense": add_expense,
    "get_expenses": get_expenses,
    "update_expense": update_expense,
    "delete_expense": delete_expense,

    "add_income": add_income,
    "get_income": get_income,
    "update_income": update_income,
    "delete_income": delete_income,

    "get_balance": get_balance,

    "get_daily_summary": get_daily_summary,
    "get_weekly_summary": get_weekly_summary,
    "get_monthly_summary": get_monthly_summary,
    "get_yearly_summary": get_yearly_summary,
    
    "set_budget": set_budget,
    "get_budget_status": get_budget_status,

    "get_category_spending" :get_category_spending,

    "get_spending_insights": get_spending_insights,

    "check_user_level_and_points": check_user_level_and_points,
}