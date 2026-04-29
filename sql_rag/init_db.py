import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "mydb.db")
SQL_FILE = os.path.join(DB_DIR, "sql_details.txt")

os.makedirs(DB_DIR, exist_ok=True)

if not os.path.exists(SQL_FILE):
    raise Exception(f"SQL file not found: {SQL_FILE}")

conn = sqlite3.connect(DB_PATH)

with open(SQL_FILE, "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print(f"Database initialized at: {DB_PATH}")