"""Quick script to delete sample articles (IDs 1-5)."""
import sqlite3, os

# Try both DB files
for db in ["data/learning.db", "data/learning_assistant.db"]:
    if not os.path.exists(db):
        print(f"  {db}: not found, skip")
        continue
    conn = sqlite3.connect(db, timeout=10)
    # Check if articles table exists
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'").fetchone()
    if not tables:
        print(f"  {db}: no articles table, skip")
        conn.close()
        continue
    c = conn.execute("DELETE FROM articles WHERE id IN (1,2,3,4,5)")
    conn.commit()
    r = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    print(f"  {db}: Deleted {c.rowcount} rows, {r} remaining")
    conn.close()
