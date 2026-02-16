"""
Seed database with fake weekly data for testing /weekly command.

Usage:
    python scripts/seed_weekly_test.py --active     # Active user scenario
    python scripts/seed_weekly_test.py --inactive   # Inactive user scenario
    python scripts/seed_weekly_test.py --restore    # Restore original DB
"""
import argparse
import shutil
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

DB_PATH = Path("data/learning.db")
BACKUP_PATH = Path("data/learning_backup.db")


def backup_db():
    """Backup current DB before seeding."""
    if BACKUP_PATH.exists():
        print(f"  Backup already exists at {BACKUP_PATH}")
        return
    shutil.copy2(DB_PATH, BACKUP_PATH)
    print(f"  ✅ Backed up → {BACKUP_PATH}")


def restore_db():
    """Restore DB from backup."""
    if not BACKUP_PATH.exists():
        print("  ❌ No backup found. Nothing to restore.")
        return
    shutil.copy2(BACKUP_PATH, DB_PATH)
    BACKUP_PATH.unlink()
    print("  ✅ Restored original DB. Backup removed.")


def seed_active():
    """Scenario A: Active user — consistent activity all week."""
    backup_db()
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    today = date.today()

    topics = [
        ("Transformer Architecture Deep Dive", "Phân tích chi tiết kiến trúc Transformer, self-attention mechanism, positional encoding và multi-head attention."),
        ("RAG Systems with LangChain", "Retrieval-Augmented Generation kết hợp LLM với external knowledge base, tăng accuracy và giảm hallucination."),
        ("Fine-tuning LLMs on Custom Data", "Các phương pháp fine-tune: LoRA, QLoRA, full fine-tuning. Trade-offs giữa cost, performance và flexibility."),
        ("Docker Best Practices 2025", "Multi-stage builds, layer caching, security scanning, distroless images. Tối ưu image size và build time."),
        ("Event-Driven Architecture Patterns", "Event sourcing, CQRS, saga pattern. Khi nào dùng message queue vs event bus."),
        ("Kubernetes Scaling Strategies", "HPA, VPA, cluster autoscaler. Metrics-based vs custom metrics scaling."),
        ("CI/CD Pipeline Optimization", "Parallel jobs, caching strategies, incremental builds. Giảm pipeline time từ 20 phút xuống 5 phút."),
        ("API Design with GraphQL", "Schema design, resolver patterns, DataLoader for N+1. So sánh REST vs GraphQL."),
        ("Python Async Deep Dive", "asyncio event loop, coroutines, tasks. Real-world patterns cho web scraping và API calls."),
        ("Database Indexing Strategies", "B-tree, hash, GIN, GiST indexes. Query plan analysis và index optimization."),
        ("Microservices Communication", "gRPC vs REST vs message queue. Service mesh với Istio. Circuit breaker pattern."),
        ("Observability Stack Setup", "Prometheus + Grafana + Loki. Distributed tracing với Jaeger. Alert rules best practices."),
    ]

    reflections = [
        ("Transformer attention rất giống search engine — query tìm relevant info từ key-value pairs", "Implement simple attention mechanism from scratch", 8),
        ("RAG giảm hallucination nhưng phụ thuộc retrieval quality — garbage in garbage out", "Test RAG pipeline với Vietnamese documents", 7),
        ("LoRA tiết kiệm resources nhưng cần chọn đúng layers để fine-tune", "So sánh LoRA vs full FT trên small dataset", 6),
        ("Docker multi-stage build giảm image size đáng kể — nên áp dụng cho tất cả projects", "Refactor existing Dockerfiles sang multi-stage", 9),
        ("Event sourcing phức tạp nhưng audit trail tuyệt vời — chỉ dùng khi thực sự cần", "Document event sourcing decision cho current project", 7),
        ("Kubernetes autoscaling cần custom metrics cho real-world use cases", "Setup custom metrics exporter cho app metrics", 6),
        ("CI/CD caching strategy cải thiện build speed rõ rệt", "Apply caching cho current CI pipeline", 8),
    ]

    article_id_start = 200  # Use high IDs to avoid conflicts

    # Insert articles: 2-3 per day for Mon-Fri, 1 for Sat-Sun
    inserted_articles = []
    for day_offset in range(7, 0, -1):
        d = today - timedelta(days=day_offset)
        weekday = d.weekday()  # 0=Mon, 6=Sun
        n_articles = 2 if weekday >= 5 else 3  # weekend: 2, weekday: 3

        for i in range(min(n_articles, len(topics) - len(inserted_articles))):
            idx = len(inserted_articles)
            if idx >= len(topics):
                break
            title, summary = topics[idx]
            aid = article_id_start + idx
            created = datetime.combine(d, datetime.min.time().replace(hour=10 + i * 3))

            conn.execute(
                """INSERT OR IGNORE INTO articles 
                   (id, raindrop_id, date, title, source_url, summary, 
                    synthesizer_output, status, queued_at, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 'sent', ?, ?)""",
                (aid, f"test_weekly_{aid}", d.isoformat(), title,
                 f"https://example.com/article-{aid}", summary,
                 summary, created.isoformat(), created.isoformat()),
            )
            inserted_articles.append((aid, title, d))

    # Insert reflections: 1 per weekday
    for i, (text, action, conf) in enumerate(reflections):
        d = today - timedelta(days=7 - i)
        if i < len(inserted_articles):
            aid = inserted_articles[i][0]
        else:
            aid = inserted_articles[0][0]
        created = datetime.combine(d, datetime.min.time().replace(hour=20))
        conn.execute(
            """INSERT INTO reflections (article_id, reflection_text, action_item, 
               confidence_score, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (aid, text, action, conf, created.isoformat()),
        )

    # Insert sessions: 1 per day
    for day_offset in range(7, 0, -1):
        d = today - timedelta(days=day_offset)
        duration = 45 if d.weekday() < 5 else 30  # weekday: 45min, weekend: 30min
        conn.execute(
            """INSERT INTO sessions (date, start_time, end_time, duration_minutes, 
               activity_type, created_at)
               VALUES (?, ?, ?, ?, 'study', ?)""",
            (d.isoformat(),
             datetime.combine(d, datetime.min.time().replace(hour=9)).isoformat(),
             datetime.combine(d, datetime.min.time().replace(hour=9, minute=duration)).isoformat(),
             duration,
             datetime.combine(d, datetime.min.time().replace(hour=9)).isoformat()),
        )

    conn.commit()
    conn.close()

    print(f"\n  📊 Scenario ACTIVE seeded:")
    print(f"     Articles: {len(inserted_articles)}")
    print(f"     Reflections: {len(reflections)}")
    print(f"     Sessions: 7")
    print(f"     Period: {(today - timedelta(days=7)).isoformat()} → {today.isoformat()}")


def seed_inactive():
    """Scenario B: Inactive user — minimal activity."""
    backup_db()
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    today = date.today()

    article_id_start = 300

    # Only 2 articles: Monday and Saturday
    mon = today - timedelta(days=6)  # ~Monday
    sat = today - timedelta(days=1)  # ~Saturday

    conn.execute(
        """INSERT OR IGNORE INTO articles 
           (id, raindrop_id, date, title, source_url, summary, 
            synthesizer_output, status, queued_at, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'sent', ?, ?)""",
        (article_id_start, f"test_weekly_{article_id_start}",
         mon.isoformat(), "Intro to Machine Learning",
         "https://example.com/ml-intro",
         "Giới thiệu cơ bản về ML: supervised, unsupervised, reinforcement learning.",
         "Tổng quan ML fundamentals.",
         datetime.combine(mon, datetime.min.time().replace(hour=14)).isoformat(),
         datetime.combine(mon, datetime.min.time().replace(hour=14)).isoformat()),
    )

    conn.execute(
        """INSERT OR IGNORE INTO articles 
           (id, raindrop_id, date, title, source_url, summary, 
            synthesizer_output, status, queued_at, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'sent', ?, ?)""",
        (article_id_start + 1, f"test_weekly_{article_id_start + 1}",
         sat.isoformat(), "Python Type Hints Guide",
         "https://example.com/type-hints",
         "Hướng dẫn sử dụng type hints trong Python: basic types, generics, protocols.",
         "Python typing overview.",
         datetime.combine(sat, datetime.min.time().replace(hour=11)).isoformat(),
         datetime.combine(sat, datetime.min.time().replace(hour=11)).isoformat()),
    )

    # 1 reflection on Monday only
    conn.execute(
        """INSERT INTO reflections (article_id, reflection_text, action_item, 
           confidence_score, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (article_id_start,
         "ML concepts khá trừu tượng, cần hands-on practice nhiều hơn",
         "Làm tutorial scikit-learn basic",
         4,
         datetime.combine(mon, datetime.min.time().replace(hour=20)).isoformat()),
    )

    # No sessions at all

    conn.commit()
    conn.close()

    print(f"\n  📊 Scenario INACTIVE seeded:")
    print(f"     Articles: 2")
    print(f"     Reflections: 1")
    print(f"     Sessions: 0")
    print(f"     Period: {(today - timedelta(days=7)).isoformat()} → {today.isoformat()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed weekly test data")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--active", action="store_true", help="Active user scenario")
    group.add_argument("--inactive", action="store_true", help="Inactive user scenario")
    group.add_argument("--restore", action="store_true", help="Restore original DB")

    args = parser.parse_args()

    if args.restore:
        restore_db()
    elif args.active:
        seed_active()
        print("\n  ▶ Start bot → test /weekly")
        print("  ▶ When done: python scripts/seed_weekly_test.py --restore")
    elif args.inactive:
        seed_inactive()
        print("\n  ▶ Start bot → test /weekly")
        print("  ▶ When done: python scripts/seed_weekly_test.py --restore")
