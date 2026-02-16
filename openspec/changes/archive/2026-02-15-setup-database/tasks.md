## 1. Project Setup

- [x] 1.1 Tạo `db/__init__.py`
- [x] 1.2 Thêm `DATABASE_PATH` vào `config.py` (default: `data/learning.db`)
- [x] 1.3 Thêm `DATABASE_PATH` vào `.env.example`
- [x] 1.4 Thêm `data/` vào `.gitignore`

> **Done khi:** `config.DATABASE_PATH` trả đúng path, `data/` folder ignored.

## 2. Schema & Initialization

- [x] 2.1 Tạo `db/models.py` với function `init_db(db_path)` — tạo database file + tất cả tables
- [x] 2.2 Implement `articles` table schema (raindrop_id UNIQUE, status DEFAULT 'queued', priority DEFAULT 0)
- [x] 2.3 Implement `reflections` table schema (FK → articles, confidence CHECK 1-10)
- [x] 2.4 Implement `sessions` table schema (activity_type, duration_minutes)
- [x] 2.5 Implement `batch_digests` table schema (article_ids JSON, deep_dive_selected JSON)
- [x] 2.6 Implement `weekly_reports` table schema (week_start, themes, gaps, suggestions)
- [x] 2.7 Auto-create parent directory nếu chưa tồn tại

> **Done khi:** `init_db()` tạo được database với 5 tables. Chạy 2 lần không bị lỗi.

## 3. Repository — Article CRUD

- [x] 3.1 Implement `add_article(db_path, **kwargs)` — insert article, return id
- [x] 3.2 Implement `get_article_by_id(db_path, article_id)` — return dict hoặc None
- [x] 3.3 Implement `get_articles_by_status(db_path, status)` — return list[dict]
- [x] 3.4 Implement `update_article_status(db_path, article_id, new_status)`
- [x] 3.5 Implement `update_article_analysis(db_path, article_id, **analysis_fields)`
- [x] 3.6 Implement `get_next_queued_article(db_path)` — oldest queued article
- [x] 3.7 Implement `get_oldest_queued_articles(db_path, n)` — oldest n queued articles
- [x] 3.8 Implement `count_articles_by_status(db_path)` — return dict {status: count}

> **Done khi:** Tất cả article functions hoạt động, duplicate raindrop_id bị reject.

## 4. Repository — Other CRUD

- [x] 4.1 Implement `add_reflection(db_path, article_id, text, action_item, confidence)` — return id
- [x] 4.2 Implement `get_reflections_by_article(db_path, article_id)`
- [x] 4.3 Implement `get_recent_reflections(db_path, days=7)`
- [x] 4.4 Implement `add_session(db_path, date, start, end, duration, activity_type)`
- [x] 4.5 Implement `get_sessions_by_date(db_path, date)`
- [x] 4.6 Implement `add_batch_digest(db_path, article_ids, digest_output, deep_dive_selected)`
- [x] 4.7 Implement `get_latest_digest(db_path)`
- [x] 4.8 Implement `add_weekly_report(db_path, week_start, themes, gaps, suggestions)`
- [x] 4.9 Implement `get_latest_report(db_path)`

> **Done khi:** Tất cả CRUD functions hoạt động. Confidence score ngoài 1-10 bị reject.

## 5. Testing & Verification

- [x] 5.1 Test `init_db()` — tạo DB, verify 5 tables tồn tại
- [x] 5.2 Test article CRUD — add, get, update status, duplicate prevention
- [x] 5.3 Test reflection CRUD — add, get by article, confidence validation
- [x] 5.4 Test queue helpers — get_next_queued, count_by_status
- [x] 5.5 Test second run — init_db() không reset data
