## Context

Hệ thống cần persistent storage cho articles, reflections, sessions, batch digests, và weekly reports. Hiện tại chưa có database layer nào. SQLite đã được chọn từ đầu (main spec) — phù hợp cho single-user local bot.

Existing code đã có: `config.py` (dotenv loader), `services/` package.

## Goals / Non-Goals

**Goals:**
- SQLite database với 5 tables đúng schema từ main spec
- Repository pattern cung cấp clean API cho các services khác
- Auto-initialization on first run
- Parameterized queries (SQL injection prevention)

**Non-Goals:**
- Schema migration system (MVP scope, schema ổn định)
- ORM (SQLAlchemy — quá nặng cho use case này)
- Connection pooling (single-user, single-thread bot)
- Async database access

## Decisions

### 1. Raw `sqlite3` thay vì ORM

**Chọn:** Python built-in `sqlite3` module
**Không chọn:** SQLAlchemy, Peewee, Tortoise ORM

**Rationale:** Anti-overengineering. 5 tables, ~15 CRUD functions — ORM chỉ thêm dependency và abstraction không cần thiết. `sqlite3` built-in, zero-cost, full control.

### 2. Repository pattern (functions, không class)

**Chọn:** Module-level functions trong `db/repository.py`
**Không chọn:** Repository class, DAO pattern

**Rationale:** Đơn giản hơn. Mỗi function nhận `db_path` hoặc connection. Dễ test, dễ import.

### 3. Database file location

**Chọn:** `data/learning.db` (configurable via `DATABASE_PATH` env var)
**Rationale:** Tách data ra khỏi source code. Folder `data/` nằm trong `.gitignore`.

### 4. Connection management

**Chọn:** Short-lived connections — mở connection mỗi operation, đóng sau khi xong.
**Không chọn:** Persistent connection, connection pool.

**Rationale:** SQLite file-based, zero network overhead. Single user → không cần pooling. `with sqlite3.connect(path) as conn:` pattern đảm bảo auto-commit/rollback.

### 5. JSON storage cho arrays

**Chọn:** TEXT fields + `json.dumps/loads` cho batch_digests.article_ids, deep_dive_selected
**Không chọn:** Separate junction tables

**Rationale:** Đơn giản hơn cho batch data. Không cần query individual IDs — chỉ cần full array. Anti-overengineering.

## Data Flow

```
Services (analyzer, raindrop, telegram)
        │
        ▼
  db/repository.py  ← clean function API
        │
        ▼
    db/models.py    ← schema init + table creation
        │
        ▼
   data/learning.db ← SQLite file
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| No migration → schema change khó | MVP scope, schema đã finalize. Nếu cần change → manual ALTER TABLE |
| Short-lived connections → overhead | Negligible cho SQLite file-based. Benchmark nếu cần |
| JSON in TEXT columns → no indexing | Chỉ dùng cho batch data, không query trực tiếp |
| Data loss nếu file bị xóa | User trách nhiệm backup. Có thể thêm backup script sau |
