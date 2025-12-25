# APPENDIX A8 - OK Computer Runbook (Canonical Overlay, Aligned)
**Version:** V5.0.2  
**Date:** 2025-12-24  
**Pilot:** Yên Lạc  

## 1. Phạm vi và nguyên tắc khóa
- Append-only (chỉ ghi thêm, không sửa lịch sử): mọi thay đổi đi qua event ledger (sổ sự kiện).
- Canonical `event_code` dùng prefix `EVT_*`; mọi tên cũ coi là alias (tên thay thế).
- `house_lifecycle_status` luôn **UPPERCASE**: `SHADOW → QUALIFIED → CLAIMED → FINANCIAL → GOLDEN`.
- Canonical metric về bằng chứng: `evidence_pass_rate` ( `risk_evidence_pass_rate` là alias ).
- **No Evidence + Bad Evidence No Pay**: không bằng chứng hoặc bằng chứng hỏng thì không trả.

## 2. Artefacts và đường dẫn registry (Registry Map)
Đặt trong thư mục `/registry` của repo:
- `registry_event_taxonomy_yenlac_v1_7_2025-12-24.yaml` (A3/P0.2)
- `registry_metrics_v5_0_2_extended_with_K7_2025-12-24.csv` (A4/P0.3)
- `registry_metric_alias_v5_0_2_2025-12-24.yaml` (PA2 - alias metrics)
- `registry_gate_matrix_v1_0_2025-12-24.yaml` (A7/P1)
- `registry_causal_edges_k0_k8_yenlac_v1_2_2025-12-24.yaml` (A1/P1)

## 3. Data contract - Event Ledger schema tối thiểu
Trường tối thiểu:
- `event_id`, `event_code`, `house_id`
- `event_at`, `ingested_at`
- `actor_role`, `actor_id`
- `evidence_pack_uri`
- `payload_json`
- `idempotency_key` (khóa chống lặp)

## 4. Preflight checklist trước Go-live
### 4.1 Registry lints (lint = kiểm quy tắc)
- Event taxonomy: `event_code` match `^EVT_[A-Z0-9_]+$`; `state_impact` dùng UPPERCASE enum.
- Metric registry: `metric_code` duy nhất; `unit` theo chuẩn `_hours/_days/_vnd/_rate/_pct`.
- Threshold/Gate: `threshold.metric_code` phải tồn tại trong metric registry (hoặc alias).
- Alias: không tạo vòng lặp; canonical phải tồn tại.
- Dependency graph: không cycle (vòng lặp phụ thuộc).

### 4.2 Smoke tests (smoke test = kiểm nhanh)
- Nạp 10 event mẫu và đảm bảo state machine chạy đúng.
- Tính 5 metric lõi: `evidence_pass_rate`, `fin_dso_days`, `vam_payout_latency_hours`, `first_time_right_rate`, `rework_rate`.
- Dashboard hiển thị đúng 3 tier (Warning/Throttle/Hard Stop).

## 5. Gate Hardening - No Evidence + Bad Evidence No Pay
Gate gợi ý:
- **G0 Consent/PII:** `Unconsented_PII_Risk=RED` hoặc `Pending_Consent_Aging_hours>48` → Hard Stop.
- **G1 Evidence:** `evidence_pass_rate` dưới ngưỡng hoặc integrity fail → Quarantine + No Pay.
- **G2 Ops SLA:** `first_time_right_rate` thấp hoặc `rework_rate` cao → Throttle.
- **G3 Finance:** `fin_dso_days` vượt ngưỡng hoặc `vam_payout_latency_hours` tăng → Throttle payout.

## 6. Kill-switch tiers và Incident SLA
- **Tier 1 Warning:** response 15 phút; action 60 phút; owner Field Runner.
- **Tier 2 Throttle:** response 5 phút; action 30 phút; owner Ops Lead / Finance Controller; backup CFO; escalate CEO nếu >2h.
- **Tier 3 Hard Stop:** response 2 phút; action 15 phút; owner Commander; backup CEO; escalate HĐQT nếu >1h.

## 7. Quarantine workflow (cách ly)
### 7.1 Trigger
- Payload thiếu trường bắt buộc theo schema event_code.
- Evidence integrity fail (hash mismatch/ảnh trùng/metadata bất thường).
- Actor role không hợp lệ.
- Temporal paradox (thời gian bất thường).

### 7.2 Triage
- Field Runner: 30 phút
- Data Lead: 60 phút
- Finance Controller: 60 phút

### 7.3 Outcomes
- ACCEPT / REJECT / ESCALATE

## 8. Rollback procedures (quay lui)
- Registry rollback: revert commit → reload registry → lints + smoke tests (timebox 2h).
- Code rollback: deploy image/tag cũ → verify kill-switch (timebox 30m).
- Data rollback: mark bad batch → reprocess từ event ledger → rebuild derived tables (timebox 4h).

## 9. Unit Test Spec cho metric engine
- Min coverage: 90%
- Must cover: boundary null/zero/extreme-high
- Owner: Data Engineer + QA Lead; review required.

