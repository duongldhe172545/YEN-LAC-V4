# Ma trận Template (Hard + Soft) — SSOT V5.0.2

## Mục tiêu
- Biến “khung” (SSOT/registry/gate) thành “chạy thật” bằng bộ template nhập liệu chuẩn.
- Hard data (dữ liệu cứng): đo được/đối soát được (UAV/evidence/job/cash).
- Soft intel (dữ liệu mềm): tình báo thực địa trước D-day (Gov/KOL/mùa vụ/TAM–SAM–SOM).

## Nguyên tắc bắt buộc (LOCKED)
- **registry-first** = sổ chuẩn trước; code đọc `registry/*.yaml|csv`.
- **append-only** = chỉ thêm; sai thì tạo event **CORRECTION** (đính chính).
- **event_code = EVT_*** + **idempotency_key** = khóa chống ghi trùng.
- **provider-neutral** = tách `provider_raw.*` và `canonical.*` (không đưa tên vendor vào canonical).
- **consent/PII**: không lưu PII khi chưa consent; `Unconsented_PII_Risk` là **kill-switch** (cầu dao ngắt).
- **gate**: No Evidence + Bad Evidence No Pay (không bằng chứng hoặc bằng chứng hỏng thì không trả).
- Evidence metric canonical: **evidence_pass_rate** (alias legacy: risk_evidence_pass_rate).

## Cách dùng nhanh (GĐ1 chạy cơm → GĐ2 chạy máy)
1) Điền template ở `templates/` (CSV) hoặc Excel Master (nếu dùng).
2) Chạy **Preflight** (bộ soi lỗi) theo `TMP_PREFLIGHT_BATCH_CHECK`.
3) Nạp event (EVT_*) theo ingest contract (append-only).
4) Nộp bằng chứng → QA → Gate → mới mở payout.

## Template Registry
Xem file: `registry/template_registry.yaml`

## Ví dụ 1 dòng (ngắn gọn)
- `TMP_EVENT_GOLDEN_PATH`:  
  `EVT_TRX_SITE_SURVEY_COMPLETED, idempotency_key=YLX01_H0001|20251224|SURVEY, house_id=YLX01_H0001, actor_id=UST_0007, event_ts=2025-12-24T09:10:00`
- `TMP_INTEL_RADAR_SNAPSHOT`:  
  `geo_unit_code=YL_XA01, snapshot_date=2025-12-20, economic_power_proxy=0.62, political_support_proxy=0.75, confidence_score=0.70`

## Thuật ngữ (Anh → Việt)
- **idempotency_key**: khóa chống ghi trùng
- **provider-neutral**: trung tính nhà cung cấp
- **append-only**: chỉ thêm, không sửa lịch sử
- **intel snapshot**: ảnh chụp tình báo tại thời điểm
- **DOR (Door Opening Rate)**: tỷ lệ mở cửa/tiếp nhận


## Bản vá v0.2 (2025-12-25) — làm rõ 3 điểm expert nêu

1) **Job Master (A3)**: `job_id` và các `*_actor_id` là **mã nội bộ** (không phải PII). PII thật (tên/số điện thoại) chỉ để `*_ref` trỏ vào **PII Vault** khi có consent.
- Thêm cột: `ust_actor_id`, `field_runner_actor_id`, `adg_actor_id` và giữ `assigned_actor_id` để tương thích.

2) **Gov Stakeholder/Engagement (B2/B3)**: bổ sung điểm số 1–5 và `outcome_reason_code` để giảm chủ quan.
- `stance_score` (1=cản nặng, 5=ủng hộ mạnh)
- `meeting_outcome_score` (1–5)
- `outcome_reason_code`: POLITICAL/TECHNICAL/LACK_BUDGET/COMPLIANCE/OTHER

3) **Influence Node/Edges (B9/B10)**: phân biệt rõ với `actor_master`.
- Nếu node là người đã có trong `actor_master` thì điền `actor_id` trong `influence_node_registry` để tránh duplicate.
- `influence_edges` bắt buộc có `from_entity_type` và `to_entity_type` (HOUSE_CLUSTER/INFLUENCE_NODE/...).

