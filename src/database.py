import os
import sqlite3

DB_PATH = "database/expense_tracker.db"

def init_db():
    os.makedirs("database", exist_ok=True)
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        currency TEXT NOT NULL,
        timezone TEXT NOT NULL,
        week_start_on TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        expense_date TEXT NOT NULL,
        expense_time TEXT,
        notes TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id integer not null,
        amount REAL NOT NULL,
        source TEXT NOT NULL,
        income_date TEXT NOT NULL,
        income_time TEXT,
        notes TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL, 
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        period TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT DEFAULT 'overall',
        is_rollover BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Optional: Insert a default user (user_id = 1) if table is empty so foreign keys work
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO users (name, currency, timezone, week_start_on, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, ("Shreyas", "INR", "Asia/Kolkata", "Monday", "2026-10-01T21:00:00"))

    connection.commit()

    # Query and print debug info
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    cursor.execute("SELECT * FROM income")
    rows1 = cursor.fetchall()

    connection.close()
    
    print("Users:", rows)
    print("Income:", rows1)
    print("Database connected and tables initialized successfully.")

# Run initialization on import
init_db()