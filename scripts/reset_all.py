"""Reset all articles to queued status."""
import sqlite3

conn = sqlite3.connect("data/learning.db", timeout=10)
c = conn.execute("""
    UPDATE articles 
    SET status = 'queued', 
        summary = NULL, 
        researcher_output = NULL, 
        architect_output = NULL, 
        skeptic_output = NULL, 
        synthesizer_output = NULL
""")
conn.commit()
total = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
print(f"Reset {c.rowcount}/{total} articles to queued")

conn.execute("DELETE FROM reflections")
conn.execute("DELETE FROM batch_digests")
conn.commit()
print("Cleared reflections + batch_digests")
conn.close()
print("Done!")
