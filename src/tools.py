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
}