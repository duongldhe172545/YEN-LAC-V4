# DEMO RUNPACK – 3 bước chạy thử (V5.0.2)

## Thuật ngữ (English → Việt)
- preflight (soi lỗi trước khi nạp)
- ingest (nạp dữ liệu vào hệ thống)
- registry-first (lấy registry làm chuẩn)
- append-only (chỉ thêm, không sửa lịch sử)
- idempotency_key (khóa chống ghi trùng)
- quarantine (cách ly bản ghi lỗi)
- unit test (kiểm thử đơn vị)

## Bước 0 – Cài môi trường
```bash
cd d2com-pilot-yen-lac
pip install -r requirements.txt
```

## Bước 1 – Preflight (soi lỗi trước khi nạp)
Chạy validate registry trước:
```bash
python code/scripts/validate_registry.py --repo_root .
```

Sau đó chạy preflight cho file events demo:
```bash
python code/scripts/preflight_templates.py --repo_root . --template_code TMP_EVENT_GOLDEN_PATH --input_csv demo_inputs/events/events_demo.csv
```

Kết quả sẽ in summary PASS/FAIL + tạo report ở `data/preflight/`.

## Bước 2 – Ingest (nạp event thật vào event store append-only)
```bash
python code/scripts/ingest_events.py --repo_root . --input_csv demo_inputs/events/events_demo.csv --source_batch_id DEMO_BATCH_001
```

Output:
- `data/event_store/event_log.jsonl` (append-only)
- `data/quarantine/quarantine_events.jsonl` (bản lỗi)

## Bước 3 – Unit Tests (đảm bảo không gãy)
```bash
pytest -q
```

## Mở OK Computer (Streamlit)
```bash
streamlit run code/ok_computer/app.py
```

Vào các page:
- Registry Viewer (xem SSOT)
- Gate Monitor (theo dõi pass/fail)
- Quarantine Queue (xem lỗi)
- Kill-Switch Panel (cầu dao ngắt)
