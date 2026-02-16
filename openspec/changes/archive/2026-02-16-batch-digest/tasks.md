## 1. Digest Prompt

- [x] 1.1 Tạo `prompts/digest.md` — prompt template cho batch digest
- [x] 1.2 Include sections: themes chung, tóm tắt từng bài, so sánh, deep-dive recommendation

> **Done khi:** Prompt file tồn tại, format phù hợp LLM call.

## 2. Digest Service

- [x] 2.1 Tạo `services/digest.py`
- [x] 2.2 Implement `create_batch_digest(db_path, n=5)` — lấy N bài queued → extract → combine → LLM → save
- [x] 2.3 Extract content cho từng bài (reuse `extract_content`)
- [x] 2.4 Combine articles text → format cho LLM prompt
- [x] 2.5 Call LLM với digest prompt
- [x] 2.6 Save result to `batch_digests` table
- [x] 2.7 Update articles status → 'digest_reviewed'
- [x] 2.8 Handle extraction failures gracefully (skip + report)

> **Done khi:** `create_batch_digest()` chạy end-to-end, lưu DB + return output.

## 3. Telegram /digest Command

- [x] 3.1 Implement `digest_command()` trong `telegram_handler.py`
- [x] 3.2 Parse args: `/digest` (default 5) hoặc `/digest <n>`
- [x] 3.3 Validate n (2-10)
- [x] 3.4 Show progress messages (extracting... → analyzing...)
- [x] 3.5 Send digest output via message splitting
- [x] 3.6 Suggest deep-dive: list `/analyze <id>` cho từng bài
- [x] 3.7 Register handler trong `build_application()`
- [x] 3.8 Update `/help` — thêm `/digest`

> **Done khi:** `/digest` command hoạt động trên Telegram.

## 4. Testing & Verification

- [x] 4.5 Compile check tất cả files
- [ ] 4.1 Test `/digest` với queue có >= 5 bài
- [ ] 4.2 Test `/digest 3` với custom count
- [ ] 4.3 Test `/digest` với queue rỗng
- [ ] 4.4 Test `/digest` khi queue ít hơn N bài
- [ ] 4.6 Test `/help` hiển thị `/digest`

> **Done khi:** Tất cả commands hoạt động + batch digest end-to-end OK
