# P2-INGEST Contract (khung nạp sự kiện)

## Mục tiêu
- **Append-only (chỉ thêm, không sửa lịch sử)**: event log chỉ append.
- **Idempotency (chống ghi trùng)**: dùng `idempotency_key` (khóa chống trùng).
- **Registry-first (lấy registry làm chuẩn)**: validate theo `registry/events.yaml`.
- **Quarantine (cách ly)**: bản ghi lỗi đi vào hàng chờ, không làm gãy luồng.

## Format input CSV
Bắt buộc các cột tối thiểu:
- `event_code` (mã sự kiện, chuẩn `EVT_*`)
- `event_ts` (thời điểm xảy ra, ISO8601, ví dụ `2025-12-24T10:00:00+07:00`)
- `idempotency_key` (khóa chống trùng) **hoặc** đầy đủ các trường trong `idempotency_key_fields` của event đó
- Các cột khác: theo `required_keys` của từng event (ví dụ `house_id`, `source_batch_id`...)

Tuỳ chọn:
- `payload_json`: JSON string, sẽ được merge vào record trước khi validate

## Output (append-only)
- `data/event_store/event_log.jsonl` : nhật ký sự kiện
- `data/event_store/idempotency_keys.txt` : index chống trùng
- `data/quarantine/quarantine_events.jsonl` : hàng chờ cách ly
- `data/audit/ingest_audit.jsonl` : audit log (nhật ký kiểm toán)

## Cách chạy
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# validate registry trước
python code/scripts/validate_registry.py --repo_root .

# ingest
python code/scripts/ingest_events.py --repo_root . --input_csv /path/to/events.csv --source_batch_id VDCD_20251224_001
```
