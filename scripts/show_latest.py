"""Show the latest article from the queue."""
import sqlite3

DB_PATH = "data/learning.db"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

row = conn.execute(
    "SELECT id, title, source_url, status, date, raw_content FROM articles ORDER BY date DESC LIMIT 1"
).fetchone()

if row:
    print(f"ID:     {row['id']}")
    print(f"Title:  {row['title']}")
    print(f"URL:    {row['source_url']}")
    print(f"Status: {row['status']}")
    print(f"Date:   {row['date']}")
    print(f"Excerpt: {(row['raw_content'] or '')[:300]}...")
else:
    print("No articles found.")

conn.close()
