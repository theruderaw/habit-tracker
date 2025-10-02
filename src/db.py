import sqlite3
from contextlib import contextmanager
from dotenv import load_dotenv
import os

# Load .env from root
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
if not DB_NAME:
    raise ValueError("DB_NAME is not set in .env")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit TEXT UNIQUE NOT NULL,
            started TEXT NOT NULL,
            days_completed INTEGER DEFAULT 0,
            time TEXT,
            goal_days INTEGER DEFAULT 0
        )
        """)

if __name__ == "__main__":
    try:
        init_db()
        print("connected")
    except Exception as e:
        print("Could not connect:", e)

