import sqlite3

DB_PATH = "database/expense_tracker.db"

def get_category_spending(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT category, SUM(amount) as total 
        FROM expenses 
        WHERE user_id = ? 
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id,)
    )
    breakdown = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"breakdown": breakdown}