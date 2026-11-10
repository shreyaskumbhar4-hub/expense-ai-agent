import sqlite3

DB_PATH = "database/expense_tracker.db"

def get_spending_insights(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get total spent
    cursor.execute("SELECT SUM(amount) as total_spent FROM expenses WHERE user_id = ?", (user_id,))
    total_result = cursor.fetchone()
    total_spent = total_result["total_spent"] if total_result and total_result["total_spent"] else 0.0
    
    # Get highest spending category
    cursor.execute(
        """
        SELECT category, SUM(amount) as total 
        FROM expenses 
        WHERE user_id = ? 
        GROUP BY category 
        ORDER BY total DESC 
        LIMIT 1
        """,
        (user_id,)
    )
    highest_category_row = cursor.fetchone()
    conn.close()
    
    highest_category = highest_category_row["category"] if highest_category_row else "None"
    highest_amount = highest_category_row["total"] if highest_category_row else 0.0
    
    return {
        "total_spent": total_spent,
        "highest_spending_category": highest_category,
        "highest_category_amount": highest_amount,
        "insight_summary": f"You have spent a total of {total_spent}. Your highest spending is in '{highest_category}' with {highest_amount}."
    }