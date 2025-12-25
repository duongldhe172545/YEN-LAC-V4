# War-room rehearsal kit (V5.0.2)

Mục tiêu: diễn tập trước go-live để "Tier 2 siết" và "Tier 3 dừng" chạy đúng, có rollback.

Bộ này dùng SSOT registry:
- registry/thresholds.yaml (ngưỡng)
- registry/runbook_actions.yaml (action cards)
- audit/*.jsonl (append-only logs)

Nguyên tắc:
- Không sửa log cũ. Mọi update là append mới.
- Thời gian phản ứng theo Incident SLA trong A8.
