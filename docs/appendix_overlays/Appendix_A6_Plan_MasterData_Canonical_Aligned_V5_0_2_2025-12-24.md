# Appendix A6 — Plan MasterData (Canonical Aligned) — D2Com Yên Lạc V5.0.2

**Version:** V5.0.2-A6  
**Build date:** 2025-12-24  
**Effective date:** 2025-12-24  
**DDAY (Pilot):** 2026-04-01  
**Mode:** append-only (chỉ thêm, không sửa lịch sử)

## 0) SSOT & chuỗi bản vá đang áp dụng
**SSOT (Single Source of Truth = nguồn sự thật duy nhất):**
- Master V5 (SPINE/MODULES) + Patch Ledger/Decision Log
- Registry (events/metrics/thresholds/alias/state_machine) là lớp “máy đọc”
- Appendix là “bằng chứng/nguồn gốc”, không dùng làm SSOT để code suy diễn

**Chuỗi bản vá dùng để align A6:**
- P0.1 — A5 Khắc bia (provider-neutral, unit chuẩn, consent/PII kill-switch, cash & finance lineage)
- P0-DATA-AGE — trục tuổi nhà (built_year + bucket) + event append-only (file: `P0-DATA-AGE.*`)
- P0.2 — A3 Event Registry (EVT_* canonical, idempotency, quarantine, event→state)
- P0.3 — A4 Algorithm Specs (K0–K8; metric_code/unit/grain/window; dependency graph)
- P1 — A1 Causal map (đồng bộ metric_code), A7 Gate hardening (No Evidence + Bad Evidence No Pay), A8 Runbook (incident SLA/rollback/unit test spec)

## 1) Mục tiêu A6 (Plan MasterData)
A6 biến “từ điển + event + KPI” thành **kế hoạch dữ liệu chạy được**:
1) Data acquisition (thu thập) có nguồn, có bằng chứng
2) Data validation (kiểm định) tự động + quarantine
3) Data delivery (bàn giao) theo data product + SLA
4) Data governance (quản trị) có owner, có rollback, có incident SLA

## 2) Data spine (xương sống dữ liệu)
### 2.1 Core entities (trục định danh)
- `house_id` (định danh vật lý) là trục drill-down bắt buộc
- `event_log_id` là bằng chứng audit (append-only)
- `job_id` là trục vận hành (thi công/khảo sát/bảo hành)
- `party_id`/`user_id_hash` là trục con người (PII chỉ lưu khi có consent)

### 2.2 House lifecycle state machine (LOCKED)
`house_lifecycle_status` ENUM UPPERCASE:  
**SHADOW → QUALIFIED → CLAIMED → FINANCIAL → GOLDEN**

**Nguyên tắc:** trạng thái chỉ được đổi bởi **EVT_*** hợp lệ (event→state mapping trong A3). Không update trực tiếp snapshot.

## 3) Data dictionary (A5) — schema canonical
### 3.1 Provider-neutral
- Tách lớp `provider_raw.*` và `canonical.*`
- Không để `vdcd_*` xuất hiện ở canonical

### 3.2 Unit & naming
- snake_case
- đơn vị chuẩn: `_hours / _days / _vnd / _rate / _pct`

### 3.3 Trục tuổi nhà (P0-DATA-AGE)
**Fields canonical:**
- built_year, last_major_renovation_year
- built_year_source, built_year_confidence_pct
- derived: house_age_bucket, house_age_years (không lưu cứng)

**Events append-only:**
- EVT_HOUSE_BUILT_YEAR_SET/UPDATED
- EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_SET/UPDATED

## 4) Event ingestion plan (A3)
### 4.1 Event schema tối thiểu (contract)
Mỗi event bắt buộc có:
- event_code (EVT_*)
- house_id
- event_at, ingested_at
- actor_role, actor_id
- evidence_pack_uri (nếu required)
- payload (schema theo từng EVT)

### 4.2 Idempotency (chống ghi trùng)
Mỗi EVT có `idempotency_key_fields`. Ingest phải:
- reject duplicate nếu key trùng trong window
- log audit append-only

### 4.3 Quarantine/Reject
- Reject: thiếu required_fields, sai enum/state, sai range (vd built_year)
- Quarantine: evidence fail, consent pending, actor không đủ quyền, anomaly

## 5) KPI/Metric plan (A4) — K0–K8
### 5.1 Metric registry
Mỗi `metric_code` bắt buộc có:
- unit, grain, window
- source_events/source_tables
- owner + test policy (unit tests)

### 5.2 Canonical evidence metric (PA2)
- canonical: **evidence_pass_rate**
- alias: risk_evidence_pass_rate → evidence_pass_rate

### 5.3 Dependency graph
KPI engine tính theo dependency graph để tránh sai thứ tự.

## 6) Gate & SLA (A7 + A8)
### 6.1 Gate levels
- GATE-0 Ready-to-Launch (D-14): PASS 100% mới go-live
- GATE-1 Validation (D+90): daily monitor + kill-switch
- GATE-1.5 Scale-ready: chuẩn nhân bản xã-in-a-box

### 6.2 No Evidence + Bad Evidence No Pay
Payout bị chặn nếu:
- thiếu evidence required
- evidence integrity fail
- consent chưa có mà có PII risk

### 6.3 Incident SLA / Rollback / Unit tests
- SLA phản ứng theo Tier 1/2/3 (A8)
- Rollback registry/code/data theo playbook (A8)
- Unit test spec: coverage + boundary null/0/extreme (A8)

## 7) Data delivery (bàn giao) — Data Products
Tối thiểu (pilot 1 xã):
- GeoJSON / API map layer (house polygon/point)
- 2D/3D asset pack (theo gói VDCD nhưng provider-neutral)
- Evidence pack index (hash + uri)
- KPI snapshots + drilldown keys

## 8) Repo implementation (để máy chạy đúng)
### 8.1 Cấu trúc thư mục chuẩn
- `registry/` : events.yaml, metrics.csv/yaml, thresholds.yaml, alias.yaml, state_machine.yaml, gate_matrix.yaml, causal_edges.yaml, lints.yaml
- `patch_ledger/` : P0.1, P0.2, P0.3, P0-DATA-AGE, P1-A8...
- `docs/` : war_room_playbook.md, go_live_checklist.md, incident_cards.md
- `code/` : ok_computer (Streamlit), scripts (validate_registry, ingest_event, trigger_kill_switch)

### 8.2 CI (Continuous Integration = kiểm tra tự động mỗi commit)
- Fail nếu registry lint FATAL
- Fail nếu threshold.metric_code không tồn tại
- Fail nếu cycle dependency graph
- Fail nếu coverage < ngưỡng

## 9) War-room (vận hành thực chiến)
### 9.1 Cadence (nhịp)
- Daily 30': Gate-1 dashboard + quarantine queue + cash/payout
- Weekly 60': KPI tree review + patch proposals
- Incident drill (2 tuần/lần): Tier-2/Tier-3

### 9.2 Bảng trách nhiệm (RACI)
- Commander: quyết định kill-switch
- Data Lead: registry + rollback registry
- Finance Controller: payout + DSO + rollback cash
- Field Runner: quarantine ops + evidence collection
- UST: lead/claim compliance

### 9.3 Go-live checklist (tóm tắt)
- PASS GATE-0 100%
- Registry lints GREEN
- Unit tests PASS
- Rollback drill PASS (timebox)
- Incident SLA owners + backups xác nhận

