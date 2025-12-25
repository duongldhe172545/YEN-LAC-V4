# APPENDIX A4 - Algorithm Specs (K0-K8) (Canonical Overlay)

Aligned to V5 + P0.1 + P0.2 + P0.3 | Date: 2025-12-24

Mục tiêu: khóa chuẩn metric_code, đơn vị đo, cửa sổ đo (window), nguồn dữ liệu (table/event), và contract công thức để code KPI engine/simulator không bịa.

**Phương án 2 (LOCK):** canonical metric cho evidence = `evidence_pass_rate`; các tên khác chỉ là alias.

## A4.0 Metadata

| Trường | Giá trị |
|---|---|
| SSOT | Hiến Pháp D2Com Yên Lạc V5 (Master) |
| Patch liên quan | P0.1 (khắc bia data), P0.2 (event registry), P0.3 (algorithm specs), P0-AGE (tuổi nhà) |
| Date | 2025-12-24 |
| Canonical house_lifecycle_status | SHADOW → QUALIFIED → CLAIMED → FINANCIAL → GOLDEN (UPPERCASE) |
| Metric naming | metric_code = snake_case lowercase; unit ∈ {hours, days, vnd, rate, pct, count} |
| Evidence metric (PA2) | evidence_pass_rate (canonical); risk_evidence_pass_rate (alias) |

## A4.1 Contract: Metric Registry

- Mỗi `metric_code` bắt buộc có: định nghĩa, entity_level, unit, window, k_level, nguồn dữ liệu (table/event), drilldown_keys.
- Metric nào xuất hiện trên dashboard/gate đều phải có định nghĩa và nguồn. Không có metric 'ma'.

## A4.2 Contract: Formula Registry

- `formula_id` là khóa tham chiếu. expression phải parse được.
- Nếu chưa đủ dữ liệu: dùng PLACEHOLDER nhưng vẫn khóa schema metric.

## A4.3 Contract: Thresholds & Kill-switch

- Kill-switch metrics phải có ngưỡng RED rõ ràng và action card trong Runbook (A8).

## A4.4 Alias policy (PA2) - Evidence metric

| alias_metric_code | canonical_metric_code | reason |
|---|---|---|
| risk_evidence_pass_rate | evidence_pass_rate | Chuẩn hóa theo gate A7 + causal edges; tránh trùng tên. |

## A4.5 Metric Catalog K0-K8

### K0 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| dedup_merge_rate | dedup_merge_rate | rate | 7d | F-K0-08 |  | NO | warn if spikes |
| evidence_pass_rate | evidence_pass_rate | rate | 7d | F-K0-10 |  | NO | warn <0.98 |
| house_age_bucket_coverage_rate | Tỷ lệ House có age_bucket | rate | 30d | F-K0-AGE-02 | EVT_HOUSE_BUILT_YEAR_SET,EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_SET | NO | NEW (P0-AGE) |
| house_built_year_coverage_rate | Tỷ lệ House có năm xây dựng | rate | 30d | F-K0-AGE-01 | EVT_HOUSE_BUILT_YEAR_SET | NO | NEW (P0-AGE) |
| house_id_match_rate | house_id_match_rate | rate | 7d | F-K1-05 |  | NO | warn < threshold |
| risk_geo_deviation_meters | risk_geo_deviation_meters | meters | point-in-time | F-H3-01 |  | NO | warn > threshold |
| roof_polygon_valid_rate | roof_polygon_valid_rate | rate | 7d | F-A1-VDCD-03 | EVT_DISC_DRONE_SCAN_CREATED | NO | Dùng cho tính diện tích/công suất; [Suy luận] ngưỡng >=90%. |
| shadow_house_id_coverage | shadow_house_id_coverage | pct | point-in-time | F-K0-01 |  | NO | warn if <0.95 |
| state_transition_latency_hours | state_transition_latency_hours | hours | 7d | F-K0-06 |  | NO | warn if rising |
| stuck_rate_critical | stuck_rate_critical | rate | 7d | F-K0-07 |  | YES | kill if >threshold |
| vdcd_pack_completion_rate | vdcd_pack_completion_rate | rate | 7d | F-A1-VDCD-01 | EVT_DISC_VDCD_PACK_CREATED,EVT_DISC_DRONE_SCAN_CREATED,EVT_DISC_LEGACY_IMPORT_CREATED | NO | Gate-0/1: thiếu pack thì CPQ/quote kém tin; [Suy luận] ngưỡng >=95%. |
| vdcd_qa_pass_rate | vdcd_qa_pass_rate | rate | 7d | F-A1-VDCD-02 | EVT_VER_VDCD_QA_PASSED,EVT_DISC_VDCD_PACK_CREATED | YES | Nếu QA fail diện rộng -> dữ liệu sai -> risk; [Suy luận] kill khi <95%. |
| verified_house_id_count | verified_house_id_count | count | point-in-time | F-K0-02 |  | NO | warn if off plan |

### K1 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| cr_qualified_to_survey_rate | Tỷ lệ Qualified → Survey | rate | 7d | F-K1-PH-01 | EVT_LEAD_QUALIFIED,EVT_SURVEY_STARTED | NO | PLACEHOLDER (A1 locked edge cần) |
| lead_citizen_org_rate | lead_citizen_org_rate | rate | 7d | F-K1-02 |  | NO |  |
| lead_created_count | Lead hôm nay (số lượng) | count | 1d | F-PULSE-LEAD-COUNT | EVT_ENG_LEAD_CREATED | NO | [Suy luận] Bổ sung kỹ thuật để Pulse có số lead hôm nay. |
| lead_platform_rate | lead_platform_rate | rate | 7d | F-K1-01 |  | NO |  |
| lead_source_ctv_rate | lead_source_ctv_rate | rate | 7d | F-K1-03 |  | NO |  |
| lead_valid_rate | lead_valid_rate | rate | 7d | F-K1-04 |  | NO | warn < threshold |
| lost_reason_distribution_json | lost_reason_distribution_json | json | point-in-time | F-K1-08 |  | NO |  |
| referral_rate | referral_rate | rate | 7d | F-K1-07 |  | NO |  |
| tcr_trust_conversion_rate | tcr_trust_conversion_rate | rate | 7d | F-K1-06 |  | NO | warn if falling |

### K2 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| adgpro_active_count | adgpro_active_count | count | point-in-time | F-K2-04 |  | NO | warn falling |
| adgpro_pass_rate | adgpro_pass_rate | rate | 7d | F-K2-05 |  | NO | warn <0.85 |
| adgpro_wallet_share | adgpro_wallet_share | rate | point-in-time | F-K4-05 |  | NO | warn falling |
| anc_active_nodes | anc_active_nodes | count | point-in-time | F-K2-03 |  | NO | warn falling |
| cancel_rate_post_close | cancel_rate_post_close | rate | 7d | F-K2-10 |  | NO | warn rising |
| first_time_right_rate | First-time-right (tỷ lệ) | rate | rolling_30d | F-OPS-01 | EVT_OPS_JOB_COMPLETED,EVT_OPS_REWORK_OPENED | YES | Đề cương nêu ≥90%. | REMAP from K? (P0.3). |
| job_started_count | Job hôm nay (số lượng bắt đầu) | count | 1d | F-PULSE-JOB-COUNT | EVT_TRX_JOB_STARTED | NO | [Suy luận] Bổ sung kỹ thuật để Pulse có số job hôm nay. |
| ops_data_latency_hours | ops_data_latency_hours | hours | 7d | F-H2-02 |  | YES | KILL if widespread >24h |
| ops_fallback_breach_count | ops_fallback_breach_count | count | point-in-time | F-H2-03 |  | YES | KILL if >0 (theo gate) |
| ops_manual_entry_flag | ops_manual_entry_flag | flag | point-in-time | F-H2-01 |  | NO | warn rising |
| ops_sla_ontime_rate | SLA On-time rate (tỷ lệ đúng hạn) | rate | 7d | F-SLA-ONTIME |  | NO | [Suy luận] Chuyển breach→ontime để causal map dễ đọc. |
| quote_in_field_minutes | Thời gian tạo báo giá tại hiện trường (phút) | minutes | 30d | F-K2-PH-01 | EVT_SURVEY_COMPLETED,EVT_QUOTE_GENERATED | NO | PLACEHOLDER (threshold registry đang có) |
| rework_rate | rework_rate | rate | 7d | F-K2-07 |  | NO | warn rising |
| sla_breach_rate | sla_breach_rate | rate | 7d | F-K2-06 |  | YES | KILL if spikes |
| sla_kitchen_door_complete_days | SLA hoàn tất cửa bếp (ngày) | days | 30d | F-K2-PH-02 | EVT_MEASURE_COMPLETED,EVT_INSTALL_COMPLETED | NO | PLACEHOLDER (threshold registry đang có) |
| sla_lead_to_survey_hours | SLA Lead→Survey (giờ) | hours | rolling_7d | F-SLA-01 | EVT_LEAD_QUALIFIED,EVT_OPS_SURVEY_STARTED | YES | Ngưỡng theo đề cương: ≤48h. |
| sla_survey_to_quote_hours | SLA Survey→Quote (giờ) | hours | rolling_7d | F-SLA-02 | EVT_OPS_SURVEY_COMPLETED,EVT_TRX_CPQ_QUOTE_CREATED | YES | Ngưỡng theo đề cương: ≤24h. |
| stockout_rate | stockout_rate | rate | 7d | F-K2-08 |  | NO | warn rising |
| supply_time_lag_days | supply_time_lag_days | days | point-in-time | F-K2-09 |  | NO | warn > threshold |
| ust_on_duty_rate | ust_on_duty_rate | rate | 7d | F-K2-01 |  | NO | warn <1.0 (pilot) |
| ust_productivity | ust_productivity | count/day | point-in-time | F-K2-02 |  | NO | warn falling |

### K3 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| avg_order_value_vnd | avg_order_value_vnd | vnd | point-in-time | F-K3-01 |  | NO |  |
| bank_approval_rate | bank_approval_rate | rate | 7d | F-K3-05 |  | NO | warn falling |
| bank_approval_time_hours | bank_approval_time_hours | hours | point-in-time | F-K3-06 |  | NO | warn >120h |
| close_rate | close_rate | rate | 7d | F-K3-03 |  | NO | warn falling |
| discount_rate | discount_rate | rate | 7d | F-K3-02 |  | NO | warn rising |
| financing_penetration | financing_penetration | rate | point-in-time | F-K3-04 |  | NO |  |
| l1_margin_per_job | l1_margin_per_job | vnd | point-in-time | F-K3-07 |  | NO | warn <0 |
| l2_cross_sell_rate | l2_cross_sell_rate | rate | 7d | F-K3-08 |  | NO |  |
| vat_goods_vnd | VAT hàng hóa (VND) | vnd | rolling_30d | F-VAT-03 | EVT_FIN_CASH_COLLECTED | NO | Chạy sau CASH_COLLECTED theo split_rules. |
| vat_install_vnd | VAT lắp đặt (VND) | vnd | rolling_30d | F-VAT-04 | EVT_FIN_CASH_COLLECTED | NO | Chạy sau CASH_COLLECTED theo split_rules. |
| vat_total_vnd | VAT Total (VND) | vnd | rolling_30d | F-VAT-02 | EVT_FIN_CASH_COLLECTED | NO | Chạy sau CASH_COLLECTED theo split_rules. |

### K4 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| cash_in_today_vnd | Cash-in hôm nay (VND) | vnd | 1d | F-PULSE-CASHIN | EVT_FIN_CASH_COLLECTED | NO | [Suy luận] Bổ sung kỹ thuật cho Pulse. |
| fin_dso_days | fin_dso_days | days | point-in-time | F-K4-01 |  | YES | KILL if >7 |
| gross_order_value_vnd | Gross Order Value (VND) | vnd | rolling_30d | F-VAT-00 | EVT_FIN_CASH_COLLECTED | NO | Chạy sau CASH_COLLECTED theo split_rules. | REMAP from K? (P0.3). |
| net_sales_basis_vnd | Doanh thu thuần basis (VND) | vnd | rolling_30d | F-VAT-01 | EVT_FIN_CASH_COLLECTED | NO | Chạy sau CASH_COLLECTED theo split_rules. | REMAP from K? (P0.3). |
| prepaid_rate | prepaid_rate | rate | 7d | F-K4-02 |  | NO |  |
| ust_working_capital_turnover_days | ust_working_capital_turnover_days | days | point-in-time | F-K4-04 |  | NO | warn rising |
| vam_payout_latency_hours | vam_payout_latency_hours | hours | 7d | F-K4-03 |  | NO | warn >24h |

### K5 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| automation_rate | Automation Rate (tỷ lệ tự động hóa) | rate | rolling_30d | F-TECH-01 |  | NO | Đề cương: Automation ≥80% để scale. |
| ust_dau_rate | Tỷ lệ UST hoạt động hằng ngày (DAU) | rate | 7d | F-K5-PH-01 | EVT_APP_SESSION_STARTED | NO | PLACEHOLDER (cần telemetry K5) |

### K6 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| complaint_resolution_time_hours | Thời gian xử lý khiếu nại (giờ) | hours | 30d | F-K6-PH-01 | EVT_COMPLAINT_OPENED,EVT_COMPLAINT_CLOSED | YES | PLACEHOLDER (threshold registry đang có) |
| consent_rate | consent_rate | rate | 7d | F-K0-03 |  | YES | kill if pending_consent_aging_hours>48 & pii_present |
| data_fraud_rate | data_fraud_rate | rate | 7d | F-K0-09 |  | YES | KILL if >threshold |
| pending_consent_aging_hours | pending_consent_aging_hours | hours | point-in-time | F-K0-04 |  | NO | warn >48 |
| risk_evidence_score | risk_evidence_score | score | point-in-time | F-H3-03 |  | NO | warn < threshold |
| risk_img_metadata_valid_flag | risk_img_metadata_valid_flag | flag | point-in-time | F-H3-02 |  | YES | kill if widespread false |
| risk_reserve_wallet_vnd | Ví dự phòng rủi ro (VND) | vnd | rolling_30d | F-SPLIT-06 | EVT_FIN_CASH_COLLECTED | NO | Chạy sau CASH_COLLECTED theo split_rules. |
| sys_kill_switch_status | Trạng thái Kill-switch (cầu dao) | enum | point-in-time | F-SYS-KILL |  | NO | [Suy luận] Metric tổng hợp để HĐQT nhìn 1 phát biết 'cầu dao' có bật không. |
| unconsented_pii_risk | unconsented_pii_risk | count | point-in-time | F-K0-05 |  | YES | KILL if >0 |
| war_room_decision_time_minutes | Thời gian ra quyết định War-room (phút) | minutes | 90d | F-SYS-PH-01 | EVT_KILL_SWITCH_TRIGGERED,EVT_WARROOM_DECISION_LOGGED | YES | PLACEHOLDER (incident SLA) |

### K7 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| product_defect_rate_post_handover | Tỷ lệ lỗi sản phẩm sau bàn giao | rate | 30d | F-K7-PH-03 | EVT_WARRANTY_OPENED,EVT_WARRANTY_CLOSED | NO | PLACEHOLDER; nếu vượt ngưỡng có thể nâng lên KILL-SWITCH ở pha scale. |
| product_gate_cycle_time_hours | Thời gian vòng đời Product Gate (giờ) | hours | 30d | F-K7-PH-02 | EVT_PG_SUBMITTED,EVT_PG_CHECK_FAILED,EVT_PG_CHECK_PASSED | NO | PLACEHOLDER. |
| product_gate_reject_rate | Tỷ lệ Product Gate reject | rate | 7d | F-K7-PH-01 | EVT_PG_CHECK_FAILED,EVT_PG_CHECK_PASSED | NO | PLACEHOLDER (chưa có event/nguồn trong pilot hiện tại). |

### K8 - Catalog

| metric_code | metric_name_vi | unit | window | formula_id | source_events | kill_switch | notes |
|---|---|---|---|---|---|---|---|
| fin_burn_rate_monthly_vnd | fin_burn_rate_monthly_vnd | vnd | 30d | F-FIN-INV-06 | EVT_FIN_OPEX_INCURRED,EVT_FIN_CAPEX_COMMITTED | NO | [Suy luận] nếu CAPEX chỉ là commit (không cash-out) thì burn dùng OPEX. |
| fin_capex_committed_cum_vnd | fin_capex_committed_cum_vnd | vnd | 30d | F-FIN-INV-04 | EVT_FIN_CAPEX_COMMITTED | NO | So với CAPEX budget để kiểm soát. |
| fin_opex_spent_cum_vnd | fin_opex_spent_cum_vnd | vnd | 30d | F-FIN-INV-05 | EVT_FIN_OPEX_INCURRED | YES | Kill khi vượt OPEX budget cap. |
| fin_pilot_capex_budget_vnd | fin_pilot_capex_budget_vnd | vnd | point-in-time | F-FIN-INV-01 | EVT_FIN_PILOT_BUDGET_SET | NO | CAPEX gồm nền tảng/thiết bị/triển khai pha đầu; Platform có thể 'ẩn' trong CAPEX. |
| fin_pilot_opex_budget_vnd | fin_pilot_opex_budget_vnd | vnd | point-in-time | F-FIN-INV-02 | EVT_FIN_PILOT_BUDGET_SET | YES | Dùng để kiểm soát burn; kill khi vượt budget cap (cần chốt cap). |
| fin_runway_days | fin_runway_days | days | point-in-time | F-FIN-INV-07 | EVT_FIN_PILOT_BUDGET_SET,EVT_FIN_CASH_COLLECTED | YES | [Suy luận] cần có cash_balance_vnd (tổng số dư ví/tiền mặt). |
| fin_working_capital_buffer_vnd | fin_working_capital_buffer_vnd | vnd | point-in-time | F-FIN-INV-03 | EVT_FIN_PILOT_BUDGET_SET | NO | [Suy luận] dùng cho runway. |
| hr_capacity_utilization_rate | hr_capacity_utilization_rate | rate | 7d | F-HR-04 | EVT_ENG_CAPACITY_SET | YES | [Suy luận] nếu >1.0 kéo dài -> quá tải -> SLA vỡ. |
| hr_field_runner_fte_count | hr_field_runner_fte_count | count | point-in-time | F-HR-02 | EVT_ENG_ROLE_ASSIGNED,EVT_ENG_ROSTER_CORE_LOCKED | NO | Pilot tối thiểu 1. |
| hr_ops_clerk_count | hr_ops_clerk_count | count | point-in-time | F-HR-03 | EVT_ENG_ROLE_ASSIGNED,EVT_ENG_ROSTER_CORE_LOCKED | NO | Checklist Gate-0 yêu cầu >=2. |
| hr_roster_fill_rate | hr_roster_fill_rate | rate | point-in-time | F-HR-01 | EVT_ENG_ROSTER_CORE_LOCKED | YES | Gate-0: nếu <100% thì không Go-Live. |

## A4.6 Gắn với Event Registry (A3)

- `source_events` phải là EVT_* canonical; nếu metric đang trỏ event legacy thì đi qua alias map ở A3.
- Nhóm Age (P0-AGE) dùng `EVT_HOUSE_BUILT_YEAR_SET`, `EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_SET` để suy ra `age_bucket`.

## A4.7 Placeholder policy

PLACEHOLDER = khóa tên + đơn vị + window + grain + nguồn dự kiến; công thức để trống hoặc mô tả bằng lời. Không bịa số.

## A4.8 Mix vào Appendix

Giữ nguyên A4 gốc (bằng chứng). Thêm file overlay canonical này vào Appendix/A4. Copy metrics CSV + metric_alias YAML vào registry/ để OK Computer đọc.