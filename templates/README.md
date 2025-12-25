# Templates Pack — SSOT V5.0.2

## Mục đích
- GĐ1 (chạy cơm): điền CSV/Excel theo tab → preflight → nạp.
- GĐ2 (chạy máy): ingest thành event log (append-only), QA evidence, gate, payout, KPI.

## Cấu trúc
- `templates/hard/` : dữ liệu cứng (nhà, event, evidence, gate, payout...)
- `templates/soft/` : dữ liệu mềm (Gov/TAM–SAM–SOM/KOL/mùa vụ...)

## Lưu ý Consent/PII
- Không ghi SĐT/CCCD trực tiếp trong template nếu chưa có consent.
- Dùng `*_ref` để trỏ tới PII vault (nếu đã consent và có quyền).

## Điểm nối khóa (keys)
- `house_id` là trục chính.
- `event_code + idempotency_key` chống trùng.
- Evidence gắn theo `evidence_id` ↔ `event_id`.

Xem chi tiết: `docs/templates/template_matrix_v5_0_2.md`


## Ghi chú v0.2 (2025-12-25)
- JOB_MASTER thêm ust_actor_id/field_runner_actor_id/adg_actor_id; actor_id là mã nội bộ (không phải PII).
- GOV_* thêm score 1–5 + outcome_reason_code.
- INFLUENCE_* thêm actor_id (optional) và entity_type cho edges.
