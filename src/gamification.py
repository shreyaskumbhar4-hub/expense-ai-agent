from datetime import date, timedelta
import sqlite3

DB_PATH = "database/expense_tracker.db"

def add_points(user_id: int, points_to_add: int = 10):
    """
    Awards points to a user and automatically levels them up 
    every 100 points, while updating streaks.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT points, level, streak, last_active_date FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"error": "User not found"}
        
    current_points, current_level, streak, last_active_date = row
    today_str = date.today().isoformat()
    
    # Streak logic
    if last_active_date == today_str:
        new_streak = streak if streak is not None else 1
    elif last_active_date == (date.today() - timedelta(days=1)).isoformat():
        new_streak = (streak if streak is not None else 1) + 1
        points_to_add += 5  # Bonus points for streak
    else:
        new_streak = 1
        
    new_points = current_points + points_to_add
    new_level = 1 + (new_points // 100)
    leveled_up = new_level > current_level
    
    cursor.execute("""
        UPDATE users 
        SET points = ?, level = ?, streak = ?, last_active_date = ? 
        WHERE id = ?
    """, (new_points, new_level, new_streak, today_str, user_id))
    
    conn.commit()
    conn.close()
    
    return {
        "points": new_points,
        "level": new_level,
        "streak": new_streak,
        "points_added": points_to_add,
        "leveled_up": leveled_up
    }

def get_user_gamification_stats(user_id: int):
    """
    Retrieves user points, current level, streak, and progress to the next level.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT points, level, streak FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"points": 0, "level": 1, "streak": 1, "points_to_next_level": 100}
        
    points, level, streak = row
    points_to_next_level = 100 - (points % 100)
    
    return {
        "points": points,
        "level": level,
        "streak": streak if streak is not None else 1,
        "points_to_next_level": points_to_next_level
    }