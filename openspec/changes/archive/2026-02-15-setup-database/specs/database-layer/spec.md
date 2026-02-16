## ADDED Requirements

### Requirement: Database initialization
Hệ thống SHALL tự động tạo SQLite database file và tất cả tables khi khởi chạy lần đầu. Nếu database đã tồn tại, hệ thống MUST giữ nguyên data hiện có.

#### Scenario: First run — database chưa tồn tại
- **WHEN** application khởi chạy lần đầu và database file chưa tồn tại
- **THEN** hệ thống tạo database file tại `DATABASE_PATH` từ config
- **THEN** tạo tất cả 5 tables: articles, reflections, sessions, batch_digests, weekly_reports

#### Scenario: Subsequent run — database đã tồn tại
- **WHEN** application khởi chạy và database file đã tồn tại
- **THEN** hệ thống MUST NOT xóa hoặc reset data hiện có
- **THEN** kết nối thành công đến database

#### Scenario: Database path từ config
- **WHEN** `DATABASE_PATH` được set trong config
- **THEN** database file MUST được tạo tại đường dẫn đó
- **THEN** parent directory MUST được tạo tự động nếu chưa tồn tại

### Requirement: Articles table schema
Table `articles` SHALL lưu trữ thông tin bài viết và kết quả phân tích từ LLM.

#### Scenario: Tạo article record mới
- **WHEN** article mới được thêm vào database
- **THEN** record MUST có các fields: id (INTEGER PK), raindrop_id (TEXT UNIQUE), date, title, source_url, raw_content, summary, key_insights, action_item, researcher_output, architect_output, skeptic_output, synthesizer_output, status (DEFAULT 'queued'), queued_at, collection_name, priority (DEFAULT 0), created_at

#### Scenario: Article status transitions
- **WHEN** article được xử lý qua các giai đoạn
- **THEN** status field MUST chỉ chứa giá trị: 'queued', 'sent', 'reflected', 'digest_reviewed'

#### Scenario: Duplicate prevention
- **WHEN** article có raindrop_id đã tồn tại trong database
- **THEN** hệ thống MUST NOT tạo duplicate record (raindrop_id là UNIQUE)

### Requirement: Reflections table schema
Table `reflections` SHALL lưu phản hồi học tập của user cho mỗi article.

#### Scenario: Tạo reflection record
- **WHEN** user hoàn thành reflection flow cho 1 article
- **THEN** record MUST có: id (PK), article_id (FK → articles), reflection_text, action_item, confidence_score (1-10), created_at

#### Scenario: Confidence score validation
- **WHEN** confidence_score được insert
- **THEN** giá trị MUST nằm trong khoảng 1–10 (CHECK constraint)

### Requirement: Sessions table schema
Table `sessions` SHALL ghi nhận thời gian học tập hàng ngày.

#### Scenario: Tạo session record
- **WHEN** user bắt đầu và kết thúc 1 phiên học
- **THEN** record MUST có: id (PK), date, start_time, end_time, duration_minutes, activity_type, created_at

#### Scenario: Activity type values
- **WHEN** session được tạo
- **THEN** activity_type MUST là 1 trong: 'reflection', 'digest_review', 'deep_dive'

### Requirement: Batch digests table schema
Table `batch_digests` SHALL lưu kết quả xử lý backlog articles.

#### Scenario: Tạo batch digest record
- **WHEN** hệ thống xử lý batch 5 articles
- **THEN** record MUST có: id (PK), article_ids (JSON array), digest_output, deep_dive_selected (JSON array), created_at

### Requirement: Weekly reports table schema
Table `weekly_reports` SHALL lưu báo cáo tổng hợp hàng tuần.

#### Scenario: Tạo weekly report record
- **WHEN** weekly synthesis chạy (Chủ nhật 23:00)
- **THEN** record MUST có: id (PK), week_start, themes_detected, knowledge_gap, build_suggestion, created_at

### Requirement: CRUD repository
Hệ thống SHALL cung cấp repository functions cho tất cả database operations. Tất cả functions MUST dùng parameterized queries để tránh SQL injection.

#### Scenario: Article CRUD
- **WHEN** code cần tương tác với articles table
- **THEN** repository MUST cung cấp: `add_article()`, `get_article_by_id()`, `get_articles_by_status()`, `update_article_status()`, `update_article_analysis()`

#### Scenario: Reflection CRUD
- **WHEN** code cần tương tác với reflections table
- **THEN** repository MUST cung cấp: `add_reflection()`, `get_reflections_by_article()`, `get_recent_reflections()`

#### Scenario: Session CRUD
- **WHEN** code cần tương tác với sessions table
- **THEN** repository MUST cung cấp: `add_session()`, `get_sessions_by_date()`

#### Scenario: Batch digest CRUD
- **WHEN** code cần tương tác với batch_digests table
- **THEN** repository MUST cung cấp: `add_batch_digest()`, `get_latest_digest()`

#### Scenario: Weekly report CRUD
- **WHEN** code cần tương tác với weekly_reports table
- **THEN** repository MUST cung cấp: `add_weekly_report()`, `get_latest_report()`

#### Scenario: Queue helpers
- **WHEN** code cần lấy articles theo queue
- **THEN** repository MUST cung cấp: `get_next_queued_article()`, `get_oldest_queued_articles(n)`, `count_articles_by_status()`
