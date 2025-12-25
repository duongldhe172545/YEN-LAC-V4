# APPENDIX A1 (OVERLAY CANONICAL) – Map nhân-quả K0–K8 (Aligned Metric Codes)
**Pilot D2Com – S2B2C | Yên Lạc | V5.0.2 overlay | Date: 2025-12-24**

## 1) Canonical IDs & invariants
- **metric_code**: snake_case (ví dụ: `fin_dso_days`). Node dùng dạng `METRIC:<metric_code>` để phân biệt loại.
- **event_code**: `EVT_<UPPERCASE>` (ví dụ: `EVT_DISC_DRONE_SCAN_CREATED`).
- **house_lifecycle_status**: `SHADOW → QUALIFIED → CLAIMED → FINANCIAL → GOLDEN` (UPPERCASE).
- **Append-only**: đổi tên phải đi qua **Alias Map** + Patch Ledger.

## 2) Alias Map (chống drift)
| Type | Legacy | Canonical | Ghi chú |
|---|---|---|---|
| metric | payout_latency_hours | vam_payout_latency_hours | A1 locked edge uses payout_latency_hours; canonical metric registry dùng vam_payout_latency_hours. |
| metric | dso_days | fin_dso_days | A1 locked edge uses dso_days; canonical dùng fin_dso_days. |
| metric | geo_deviation_meters | risk_geo_deviation_meters | A1 node uses geo_deviation_meters; canonical metric registry dùng risk_geo_deviation_meters. |
| metric | roster_fill_rate | hr_roster_fill_rate | A1 node uses roster_fill_rate; canonical metric registry dùng hr_roster_fill_rate. |
| metric | field_runner_utilization | hr_capacity_utilization_rate | A1 node uses field_runner_utilization; canonical metric registry có hr_capacity_utilization_rate. |
| metric | monthly_burn_rate_vnd | fin_burn_rate_monthly_vnd | A1 node uses monthly_burn_rate_vnd; canonical metric registry dùng fin_burn_rate_monthly_vnd. |
| metric | runway_days | fin_runway_days | A1 node uses runway_days; canonical metric registry dùng fin_runway_days. |
| metric | risk_evidence_pass_rate | evidence_pass_rate | Threshold registry dùng risk_evidence_pass_rate; metric registry dùng evidence_pass_rate. |
| metric | dau_rate_ust | ust_dau_rate | A1 locked edge dùng dau_rate_ust; metric adoption chưa có trong registry => tạo placeholder ust_dau_rate. |
| metric | cr_qualified_to_survey | cr_qualified_to_survey_rate | A1 locked edge dùng cr_qualified_to_survey; chưa có trong metric registry => tạo placeholder. |


## 3) Node Dictionary (metric list)
Danh sách đầy đủ nằm trong file CSV đi kèm:
- `registry_metrics_plus_placeholders_v5_0_2_2025-12-24.csv`

## 4) Edge Registry (causal edges)
| edge_id | from_metric | to_metric | sign | lag_days | weight | status | explain_vi |
|---|---|---|---|---|---|---|---|
| E001 | unconsented_pii_risk | sys_kill_switch_status | + | 0 | 1.0 | LOCKED | Giữ PII chưa consent quá 48h => bật cầu dao (kill-switch). |
| E002 | ops_manual_entry_flag | data_fraud_rate | + | 3 | 0.7 | LOCKED | Nhập tay/fallback nhiều => tăng nhầm/gian lận. |
| E003 | data_fraud_rate | evidence_pass_rate | - | 3 | 0.6 | INFERRED | Gian lận tăng => tỷ lệ bằng chứng đạt giảm. |
| E004 | vam_payout_latency_hours | ust_on_duty_rate | - | 7 | 0.6 | INFERRED | Trả thưởng chậm => lực lượng nguội, ít hoạt động. |
| E005 | fin_dso_days | fin_runway_days | - | 30 | 0.6 | INFERRED | Thu tiền chậm => runway giảm => phải giảm nhịp ra quân. |
| E101 | vdcd_pack_completion_rate | sla_survey_to_quote_hours | - | 7 | 0.4 | INFERRED | Có đủ gói dữ liệu VDCD => ra báo giá nhanh hơn (ít khảo sát lại). |
| E102 | vdcd_qa_pass_rate | first_time_right_rate | + | 7 | 0.3 | INFERRED | Dữ liệu chuẩn hơn => làm đúng ngay lần đầu tăng. |
| E201 | hr_roster_fill_rate | ops_sla_ontime_rate | + | 3 | 0.5 | INFERRED | Đủ người => on-time tốt hơn. |
| E202 | hr_capacity_utilization_rate | rework_rate | + | 7 | 0.4 | INFERRED | Quá tải => làm ẩu => rework tăng. |
| E301 | PARAM:os_pct_default | fin_burn_rate_monthly_vnd | + | 30 | 0.7 | LOCKED | OS% cao => burn tăng. |
| E302 | fin_runway_days | PARAM:marketing_intensity | - | 30 | 0.5 | INFERRED | Runway thấp => giảm cường độ marketing. |
| E303 | PARAM:marketing_intensity | lead_created_count | + | 7 | 0.6 | INFERRED | Marketing mạnh => lead tăng. |
| E040 | vam_payout_latency_hours | anc_active_nodes | - | 7 | 0.85 | LOCKED | Trả thưởng chậm, người đem lead bỏ, lead tụt. |
| E042 | fin_dso_days | adgpro_active_count | - | 14 | 0.5 | LOCKED | Tiền về chậm, thợ ưu tiên job ngoài. |
| E021 | rework_rate | fin_dso_days | + | 7 | 0.6 | LOCKED | Làm lại nhiều, nghiệm thu chậm, tiền về chậm. |
| E022 | sla_lead_to_survey_hours | cr_qualified_to_survey_rate | - | 7 | 0.5 | LOCKED | Khảo sát chậm, khách nguội, rơi lead. |
| E050 | ust_dau_rate | ops_manual_entry_flag | - | 3 | 0.6 | LOCKED | UST dùng app nhiều thì ít nhập tay, dữ liệu sạch hơn. |


File YAML đi kèm để code đọc trực tiếp:
- `registry_causal_edges_k0_k8_yenlac_v1_2_2025-12-24.yaml`

## 5) Edge Backlog (K9/K10)
- K9 Product Quality: `defect_rate`, `warranty_claim_rate`, `product_return_rate` (chưa có telemetry chuẩn trong pilot).
- K10 Replication: `replication_success_rate`, `time_to_clone_commune_days` (khóa sau Gate-1.5).
