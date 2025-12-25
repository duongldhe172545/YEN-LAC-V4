# War-room Playbook — Pilot Yên Lạc (V5.0.2)

**Build date:** 2025-12-24  
**DDAY:** 2026-04-01

## 1) Mục tiêu
Giữ 4 engine không gãy:
1) Revenue engine (SOM lặp lại)
2) Ops engine (đúng hẹn, ít làm lại)
3) Cash & Incentive (tiền về đúng nhịp, chi trả theo SLA)
4) Data & Social (dữ liệu sạch/không gian lận, khiếu nại xử nhanh, địa phương không “tuýt còi”)

## 2) Nhịp vận hành (Cadence)
### Daily (30’)
- 10’: Gate-1 dashboard (đỏ/vàng/xanh)
- 10’: Quarantine queue (top 10 case)
- 10’: Cash/payout (payout_latency_hours, dso_days)

### Weekly (60’)
- KPI tree K0–K8 review (drilldown đến house_id/event_id)
- Patch proposals (nếu có drift/thiếu)
- Capacity plan (EPC→ADG Pro handover)

### Incident drill (2 tuần/lần)
- Kịch bản Tier-2 (Throttle) và Tier-3 (Hard Stop)
- Bắt buộc chạy rollback rehearsal (registry rollback + code rollback)

## 3) Bảng vai trò (RACI tối thiểu)
- Commander: A (Accountable = chịu trách nhiệm cuối) cho kill-switch
- Data Lead: A/R cho registry, lint, rollback registry
- Finance Controller: A/R cho payout, DSO, rollback cash
- Field Runner: A/R cho quarantine ops + evidence
- UST: A/R cho lead/claim compliance

## 4) Quy tắc “không thương lượng”
- Append-only: không sửa lịch sử
- Canonical: EVT_* (event_code), metric_code theo registry
- No Evidence + Bad Evidence No Pay
- No consent + PII risk = kill-switch

## 5) Dashboard tối thiểu (để go-live)
- K0 Data Spine: verified_house_count, duplicate_rate, pending_consent_aging_hours
- K2 Ops: first_time_right_rate, rework_rate, sla_breach_rate
- K4 Cash: payout_latency_hours, dso_days, burn_rate_vnd
- K6 Gov/Safety: unconsented_pii_risk (kill-switch), complaint_resolution_time_hours
- Gate: evidence_pass_rate (canonical), quarantine_backlog_count

## 6) Output mỗi ngày
- Daily log (append-only): quyết định + lý do + metric snapshot + action owners
