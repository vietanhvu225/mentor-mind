"""Reset all analyzed articles back to 'queued' for re-processing."""
import sqlite3

DB_PATH = "data/learning.db"
conn = sqlite3.connect(DB_PATH)

# Find tables
print("=== Tables ===")
for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(f"  {row[0]}")

# Show current status counts
print("\n=== Before ===")
for row in conn.execute("SELECT status, count(id) FROM articles GROUP BY status"):
    print(f"  {row[0]}: {row[1]}")

# Reset all non-queued back to queued
result = conn.execute("UPDATE articles SET status = 'queued' WHERE status != 'queued'")
conn.commit()
print(f"\n→ Reset {result.rowcount} articles to 'queued'")

# Verify
print("\n=== After ===")
for row in conn.execute("SELECT status, count(id) FROM articles GROUP BY status"):
    print(f"  {row[0]}: {row[1]}")

conn.close()
print("\nDone!")
