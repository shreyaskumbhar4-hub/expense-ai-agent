import os
import sqlite3
from datetime import datetime, timedelta

DB_PATH = "database/expense_tracker.db"

def _get_connection():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def set_budget(user_id: int, period: str, amount: float, category: str = "overall", is_rollover: int = 0):
    conn = _get_connection()
    cursor = conn.cursor()
    
    # Check if budget already exists for this period & category
    cursor.execute(
        """
        SELECT id FROM budgets WHERE user_id = ? AND period = ? AND category = ?
        """,
        (user_id, period, category)
    )
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute(
            """
            UPDATE budgets SET amount = ?, is_rollover = ? WHERE user_id = ? AND period = ? AND category = ?
            """,
            (amount, is_rollover, user_id, period, category)
        )
    else:
        cursor.execute(
            """
            INSERT INTO budgets (user_id, period, amount, category, is_rollover) VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, period, amount, category, is_rollover)
        )
        
    conn.commit()
    conn.close()
    return {"status": "success", "period": period, "amount": amount, "category": category, "is_rollover": is_rollover}

def calculate_rollover_amount(user_id: int, period: str, base_limit: float) -> float:
    """
    Calculates unspent money from the previous period if rollover is enabled.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    
    now = datetime.now()
    rollover_added = 0.0
    
    if period == "daily":
        yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND date(expense_date) = ?",
            (user_id, yesterday_str)
        )
        res = cursor.fetchone()
        spent_yesterday = res["total"] if res and res["total"] else 0.0
        
        # If they spent less than the base limit yesterday, the difference rolls over
        if spent_yesterday < base_limit:
            rollover_added = base_limit - spent_yesterday
            
    conn.close()
    return rollover_added

def get_budget_status(user_id: int, period: str = "daily"):
    conn = _get_connection()
    cursor = conn.cursor()
    
    # Fetch budget limit and rollover flag
    cursor.execute(
        """
        SELECT amount, is_rollover FROM budgets WHERE user_id = ? AND period = ? AND category = 'overall'
        """,
        (user_id, period)
    )
    budget_row = cursor.fetchone()
    if not budget_row:
        conn.close()
        return {"error": f"No {period} budget set yet."}
    
    base_limit = budget_row["amount"]
    is_rollover = budget_row["is_rollover"] if "is_rollover" in budget_row.keys() else 0
    
    # Calculate rollover bonus if enabled
    rollover_bonus = calculate_rollover_amount(user_id, period, base_limit) if is_rollover else 0.0
    budget_limit = base_limit + rollover_bonus
    
    now = datetime.now()
    
    # Calculate spending based on period
    if period == "daily":
        target_str = now.strftime("%Y-%m-%d")
        cursor.execute(
            """
            SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND date(expense_date) = ?
            """,
            (user_id, target_str)
        )
    elif period == "weekly":
        start_of_week = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
        end_of_week = (now + timedelta(days=6 - now.weekday())).strftime("%Y-%m-%d")
        cursor.execute(
            """
            SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND date(expense_date) BETWEEN ? AND ?
            """,
            (user_id, start_of_week, end_of_week)
        )
    elif period == "monthly":
        target_month = now.strftime("%Y-%m")
        cursor.execute(
            """
            SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND strftime('%Y-%m', expense_date) = ?
            """,
            (user_id, target_month)
        )
    elif period == "yearly":
        target_year = now.strftime("%Y")
        cursor.execute(
            """
            SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND strftime('%Y', expense_date) = ?
            """,
            (user_id, target_year)
        )
    
    result = cursor.fetchone()
    spent = result["total"] if result and result["total"] else 0.0
    conn.close()
    
    remaining = budget_limit - spent
    percentage = (spent / budget_limit) * 100 if budget_limit > 0 else 0
    
    return {
        "period": period,
        "base_limit": base_limit,
        "rollover_bonus": rollover_bonus,
        "budget_limit": budget_limit,
        "spent": spent,
        "remaining": remaining,
        "percentage_used": round(percentage, 2)
    }