import sqlite3

conn = sqlite3.connect("messages.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    message TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database initialized.")
