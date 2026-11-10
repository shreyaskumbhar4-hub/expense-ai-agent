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


from src.budget import (
    set_budget, 
    get_budget_status
)

from src.analytics import get_category_spending

from src.insights import get_spending_insights


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

    "get_spending_insights": get_spending_insights
}