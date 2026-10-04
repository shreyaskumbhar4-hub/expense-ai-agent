import os
import sqlite3

connection = sqlite3.connect("database/expense_tracker.db")

connection.execute("""
create table if not exists users(
    id integer primary key autoincrement,
    name text not null,
    currency text not null,
    timezone text not null,
    week_start_on text not null,
    created_at text not null
    )

""")
connection.execute("""
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

connection.execute("""
create table if not exists income (
    id integer primary key autoincrement,
    user_id integer not null,
    amount real not null,
    source text not null,
    income_date text not null,
    income_time text,
    notes text,
    status text not null,
    created_at text not null,
    updated_at text not null, 
    foreign key (user_id) references users(id)
)
""")
# connection.execute("""
# INSERT INTO users (
#     name,
#     currency,
#     timezone,
#     week_start_on,
#     created_at
# )
# VALUES (?, ?, ?, ?, ?)
# """, (
#     "Shreyas",
#     "INR",
#     "Asia/Kolkata",
#     "Monday",
#     "2026-10-01T21:00:00"
# ))
# connection.execute("""
# INSERT INTO income (
#     user_id,
#     amount,
#     source,
#     income_date,
#     income_time,
#     notes,
#     status,
#     created_at,
#     updated_at
# )
# VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
# """, (
#     1,
#     30000,
#     "Salary",
#     "2026-10-01",
#     None,
#     None,
#     "confirmed",
#     "2026-10-01T21:00:00",
#     "2026-10-01T21:00:00"
# ))
# connection.execute("DELETE FROM income")

cursor = connection.execute("""
SELECT * FROM users
""")
rows = cursor.fetchall()


cursor1 = connection.execute("""
SELECT * FROM income
""")
rows1 = cursor1.fetchall()

connection.commit()
print(rows)
print(rows1)
print("Database connected successfully")
connection.close()