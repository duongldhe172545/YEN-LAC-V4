# APPENDIX A7 (OVERLAY CANONICAL) – Gate Hardening Matrix (Aligned Metric Codes)
**Pilot D2Com – S2B2C | Yên Lạc | V5.0.2 overlay | Date: 2025-12-24**

## 1) Non-negotiable: No Evidence + Bad Evidence No Pay
- Evidence taxonomy (bằng chứng) tối thiểu: `EV_TIME, EV_ACTOR, EV_GEO, EV_LINK, EV_HASH`.
- Event có `evidence_required` mà thiếu evidence ⇒ **reject/quarantine** ⇒ **không payout**.
- Evidence fail integrity (hash fail/EXIF mismatch/geo mismatch) ⇒ quarantine + audit + clawback nếu đã payout.

## 2) Gate control matrix

### Gate-0 (Ready-to-Launch)
| Gate item | Metric checks | Event hooks | If breach |
|---|---|---|---|
| Định danh House_ID sạch (Data spine) | shadow_house_id_coverage (TBD)<br>verified_house_id_count (TBD) | EVT_DISC_DRONE_SCAN_CREATED<br>EVT_VER_ID_VERIFIED | Nếu coverage thấp: dừng mở rộng, fix ingest/dedup. |
| Consent & PII (đồng ý & dữ liệu nhạy cảm) | consent_rate (TBD)<br>pending_consent_aging_hours (G:≤48h; Y:48–72h; R:>72h hoặc có PII khi chưa consent (KILL theo Unconsented_PII_Risk); KILL:True)<br>unconsented_pii_risk (TBD) | EVT_VER_CONSENT_REQUESTED<br>EVT_VER_CONSENT_OTP_VERIFIED<br>EVT_VER_CONSENT_REVOKED | No consent: không lưu PII; aging>48h: ép xin consent hoặc xóa. |
| Evidence No Pay (bằng chứng) | evidence_pass_rate (G:≥98% [Suy luận]; Y:95%–<98% [Suy luận]; R:<95% [Suy luận] (đỏ); KILL:True)<br>data_fraud_rate (G:≤1% [Suy luận]; Y:1%–3% [Suy luận]; R:>3% [Suy luận] (KILL); KILL:True)<br>ops_fallback_breach_count (G:0; Y:1–2; R:≥3 hoặc bất kỳ job quá 24h không reconcile bị khóa thưởng ngày đó (KILL theo quy ước vận hành); KILL:True) | EVT_EVIDENCE_PACK_UPLOADED<br>EVT_EVIDENCE_HASH_VERIFIED | Bad/no evidence => quarantine/reject, không payout. |
| Ops & SLA tối thiểu | sla_lead_to_survey_hours (G:≤48h; Y:48–72h; R:>72h (đỏ) và kéo dài sẽ kích hoạt kill-switch SLA vỡ; KILL:True)<br>sla_survey_to_quote_hours (G:≤24h; Y:24–48h; R:>48h (đỏ); KILL:True)<br>ops_sla_ontime_rate (TBD)<br>rework_rate (TBD) | EVT_SURVEY_STARTED<br>EVT_SURVEY_COMPLETED<br>EVT_JOB_COMPLETED | SLA vỡ => throttle lead, tăng EPC dẫn đường. |
| HR/Capacity (chịu tải) | hr_roster_fill_rate (G:=100% (Gate-0); Y:90–<100% [Suy luận]; R:<90% [Suy luận] (KILL); KILL:True)<br>hr_capacity_utilization_rate (G:≤1.0; Y:1.0–1.2 [Suy luận]; R:>1.2 [Suy luận] (KILL); KILL:True) | EVT_HR_ROSTER_SNAPSHOT | Thiếu roster => không Go-Live. |
| Finance safety (đốt tiền & runway) | fin_burn_rate_monthly_vnd (TBD)<br>fin_runway_days (G:≥90 ngày [Suy luận]; Y:60–<90 ngày [Suy luận]; R:<60 ngày [Suy luận] (KILL); KILL:True)<br>fin_dso_days (G:≤7 ngày; Y:8–10 ngày; R:>10 ngày (KILL) / hoặc >7 ngày nếu pilot chốt kill cứng; KILL:True)<br>vam_payout_latency_hours (G:≤24h [Suy luận]; Y:24–48h [Suy luận]; R:>48h [Suy luận] (đỏ); KILL:True) | EVT_FIN_TXN_SETTLED<br>EVT_PAYOUT_EXECUTED | Runway<60d hoặc DSO>7 => Hard Stop. |
| Age coverage (tuổi nhà) | house_built_year_coverage_rate (TBD)<br>house_age_bucket_coverage_rate (TBD) | EVT_HOUSE_BUILT_YEAR_SET | Thiếu tuổi nhà => không được chốt thiết kế/đề xuất cross-sell theo vòng đời. |


### Gate-1 (Day-90 Validation)
| Gate item | Metric checks | Event hooks | If breach |
|---|---|---|---|
| Tiền thật (cash loop) | fin_dso_days (G:≤7 ngày; Y:8–10 ngày; R:>10 ngày (KILL) / hoặc >7 ngày nếu pilot chốt kill cứng; KILL:True)<br>vam_payout_latency_hours (G:≤24h [Suy luận]; Y:24–48h [Suy luận]; R:>48h [Suy luận] (đỏ); KILL:True) | EVT_FIN_TXN_SETTLED<br>EVT_PAYOUT_EXECUTED | Nếu DSO xấu: siết điều khoản/thu trước/giảm rủi ro. |
| Job thật (ops loop) | ops_sla_ontime_rate (TBD)<br>rework_rate (TBD) | EVT_JOB_COMPLETED<br>EVT_QA_PASSED | Rework tăng => audit thợ + chuẩn hóa quy trình. |
| Network thật (UST/ANC/ADGPro) | anc_active_nodes (TBD)<br>adgpro_active_count (TBD) | EVT_ANC_NODE_ACTIVE<br>EVT_ADGPRO_JOB_ACCEPTED | Payout chậm => network rơi; fix payout cadence. |
| Data & Fraud (an toàn) | data_fraud_rate (G:≤1% [Suy luận]; Y:1%–3% [Suy luận]; R:>3% [Suy luận] (KILL); KILL:True)<br>ops_manual_entry_flag (TBD) | EVT_AUDIT_FLAGGED<br>EVT_MANUAL_OVERRIDE_USED | Fraud spike => kill-switch, quarantine toàn bộ job liên quan. |
| Adoption (K5 placeholder) | ust_dau_rate (TBD) | EVT_APP_SESSION_STARTED | UST không bám app => dữ liệu drift; bắt buộc training + chứng cứ upload. |


### Gate-1.5 (Scale-Ready)
| Gate item | Metric checks | Event hooks | If breach |
|---|---|---|---|
| Scale-ready (nhân bản) | replication_success_rate (TBD)<br>time_to_clone_commune_days (TBD) | EVT_REPLICATION_RUN_STARTED<br>EVT_REPLICATION_RUN_COMPLETED | PLACEHOLDER: khóa sau khi có 2 xã chạy ổn. |


## 3) Incident Response SLA (SLA phản ứng sự cố)
| Tier | Response time | Action time | Backup owner | Escalation |
|---|---|---|---|---|
| Tier_1_Warning | 15 phút | 1h | Deputy Head of Risk | N/A |
| Tier_2_Throttle | 5 phút | 30 phút | CFO | CEO nếu >2h chưa resolve |
| Tier_3_Hard_Stop | 2 phút | 15 phút | CEO | HĐQT nếu >1h chưa mở lại |


## 4) Rollback procedures (quay lui)
| Type | Condition | Steps (tóm tắt) | Max time | Owner |
|---|---|---|---|---|
| Registry rollback | Alias governance violation / fatal linter error | Git revert; reload registry; smoke tests | 2h | Data Lead |
| Code rollback | Bug affecting payout/fraud detection | Rollback Docker image; verify kill-switch; rerun KPI baseline | 30 phút | Tech Lead |


## 5) Drift report cần vá tiếp
Các metric đang có trong threshold registry nhưng chưa có metric registry (cần add placeholder hoặc alias):
- sla_kitchen_door_complete_days, quote_in_field_minutes, war_room_decision_time_minutes, risk_evidence_pass_rate, complaint_resolution_time_hours

File YAML đi kèm để code/ops đọc:
- `registry_gate_matrix_v1_0_2025-12-24.yaml`
