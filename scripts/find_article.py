import sqlite3
conn = sqlite3.connect("data/learning.db")
rows = conn.execute(
    "SELECT id, title, source_url FROM articles WHERE source_url LIKE '%facebook%' ORDER BY id"
).fetchall()
for r in rows:
    print(f"[{r[0]}] {r[1][:70]}")
    print(f"     {r[2][:90]}")
    print()
