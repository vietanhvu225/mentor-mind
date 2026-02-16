Strategic Intelligence System
Roadmap (Future Product)

1. Vision

Xây dựng hệ thống AI intelligence phục vụ:

Market validation

Business opportunity scan

Startup ideation

Team simulation

Tạo nền tảng cho việc ra quyết định chiến lược dựa trên AI.

Điều kiện kích hoạt: Chỉ bắt đầu sau khi MentorMind đã chạy ổn định 30–60 ngày.

2. Điều kiện tiên quyết

Habit học ổn định (≥ 25/30 ngày streak)

Reflection đều đặn

Có data thật từ MentorMind

Muốn scale persona / automation

3. Persona Design

Bot A – AI Thực Chiến
- Tactical analysis
- Ứng dụng thực tế ngay

Bot B – Business Overview
- Business validation
- Market opportunity
- Revenue potential

Bot C – Content Angle
- Content idea generation
- Audience insight
- Distribution strategy

Bot D – Chief of Staff Agent
- Tổng hợp từ 3 bot trên
- Prioritize actions
- Strategic recommendation

(Có thể dùng agent framework như PicoClaw hoặc tương đương)

4. Tech Stack (Dự kiến)

Agent Framework: PicoClaw hoặc tương đương

Multi-agent engine

Skill system

Tool calling

Cron scheduling

Workspace memory

Gateway abstraction

Không dùng:
❌ Microservice architecture (trừ khi scale team)

5. Architecture

Raindrop / Multiple Sources
     ↓
Agent Engine (PicoClaw)
     ↓
Custom Skills:
   - Tactical Agent
   - Business Agent
   - Content Agent
   - Chief of Staff Agent
     ↓
SQLite / Extended Memory
     ↓
Telegram Gateway

Note về Raindrop Integration:
- MentorMind đang scan ALL Raindrop collections
- Khi SIS bắt đầu, cần implement filter logic (tags hoặc collections riêng)
  để phân biệt bài learning vs business/strategy
- Có thể dùng: Raindrop tags (VD: #learning, #business)
  hoặc collections riêng cho mỗi product

6. Capabilities (Phase 2+)

Multi-agent debate

Web search integration

Deep dive mode

Market scan

7. Budget

Dự kiến: $30–80 / tháng

Tùy thuộc vào:

Multi-agent debate frequency

Web search usage

Deep dive mode activation

8. Future Evolution – Full Strategic Intelligence

Tách riêng hoàn toàn thành product độc lập.

Mục tiêu:

Market validation tự động

Business opportunity scan

Startup ideation pipeline

Team simulation

Có thể:

Full PicoClaw

Hoặc hệ agent riêng

Hoặc microservice architecture

9. Quyết định Kiến Trúc (Chốt)

Chỉ bắt đầu khi MentorMind ổn định

Có thể tích hợp PicoClaw làm agent engine

Budget cao hơn – ưu tiên strategic value

Không scale team khi chưa ổn định cá nhân
