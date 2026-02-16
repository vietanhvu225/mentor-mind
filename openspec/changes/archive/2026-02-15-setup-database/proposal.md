## Why

Hệ thống cần lưu trữ articles, reflections, sessions, batch digests, và weekly reports. SQLite là lựa chọn đã quyết định — đơn giản, file-based, không cần server. Hiện tại chưa có database layer nào. Đây là nền tảng cho mọi change sau (Telegram bot, scheduler, reflection system).

## What Changes

- Tạo `db/models.py` — SQLite schema initialization (5 tables)
- Tạo `db/repository.py` — CRUD operations cho tất cả tables
- Tạo `db/__init__.py` — package init
- Thêm database path vào `config.py`
- Auto-create database file + tables on first run

## Capabilities

### New Capabilities
- `database-layer`: SQLite schema (5 tables: articles, reflections, sessions, batch_digests, weekly_reports) và repository pattern cho CRUD operations.

### Modified Capabilities
- None

## Không làm
- Migration system (không cần cho MVP, schema sẽ ổn định)
- ORM (SQLAlchemy quá nặng, dùng raw sqlite3)
- Connection pooling (single-user bot)
- Backup automation

## Impact

- **New files:** `db/models.py`, `db/repository.py`, `db/__init__.py`
- **Modified:** `config.py` (thêm `DATABASE_PATH`)
- **Dependencies:** Không thêm package mới (sqlite3 built-in)
- **Data:** Database file tạo tự động tại `data/learning.db`
