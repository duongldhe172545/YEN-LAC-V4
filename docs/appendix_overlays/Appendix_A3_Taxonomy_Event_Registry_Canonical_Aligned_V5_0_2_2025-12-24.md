# APPENDIX A3 - Taxonomy & Event Registry (Canonical Overlay)

Aligned to V5 + P0.1 + P0.2 | Date: 2025-12-24

Mục tiêu: khóa danh mục sự kiện (EVT_*), schema tối thiểu, alias map, quy tắc quarantine/reject, và bảng event→state để code/ops không drift.

## A3.0 Metadata

| Trường | Giá trị |
|---|---|
| SSOT | Hiến Pháp D2Com Yên Lạc V5 (Master) |
| Patch liên quan | P0.1 (khắc bia data), P0.2 (event registry), P0-AGE (tuổi nhà), A7 gate hardening |
| Version | v1.7 |
| generated_at | 2025-12-24T09:00:00 |
| Canonical house_lifecycle_status | SHADOW → QUALIFIED → CLAIMED → FINANCIAL → GOLDEN (UPPERCASE) |
| Naming | event_code = EVT_[A-Z0-9_]+ (UPPERCASE) |

## A3.1 Event Schema tối thiểu

| field | type | required | notes |
|---|---|---|---|
| event_id | string/uuid | YES | ID duy nhất cho event (append-only). |
| event_code | string | YES | Canonical EVT_*. |
| event_at | datetime | YES | Thời điểm xảy ra tại hiện trường/hệ thống. |
| ingested_at | datetime | YES | Thời điểm hệ thống nhận event. |
| house_id | string | YES (nếu entity_scope=house) | House_ID canonical. |
| job_id | string | NO | Job/đơn thi công (nếu có). |
| actor_role | enum | YES | Vai trò (UST/Field Runner/ADG Pro/EPC...). |
| actor_id | string | YES | Định danh người làm. |
| payload_json | json | YES | Payload theo schema của từng EVT_*. |
| evidence_pack_uri | string/uri | Conditional | Bắt buộc nếu event yêu cầu evidence. |
| idempotency_key | string/hash | YES | Hash từ idempotency_key_fields để chống lặp. |
| schema_version | string | YES | Version schema event taxonomy. |

## A3.2 Canonical States & Transition

House lifecycle states (LOCKED): SHADOW / QUALIFIED / CLAIMED / FINANCIAL / GOLDEN

## A3.3 Evidence taxonomy (tối thiểu)

| evidence_code | vi |
|---|---|
| EV_TIME | Dấu thời gian (event_at + ingested_at) |
| EV_ACTOR | Định danh người làm (actor_id + role) |
| EV_GEO | Tọa độ (geo_point) + geofence_match |
| EV_PHOTO_EXIF | Ảnh có EXIF gốc + hash ảnh |
| EV_LINK | Gắn đúng khóa (house_id/lead_id/job_id) |

## A3.4 Alias Map (tên cũ → tên chuẩn)

| legacy_code | canonical_event_code |
|---|---|
| EVT_LEAD_QUALIFIED | EVT_VER_HOUSE_QUALIFIED |
| EVT_OPS_JOB_COMPLETED | EVT_TRX_HANDOVER_SIGNED |
| EVT_OPS_REWORK_OPENED | EVT_OPS_REWORK_OPENED |
| EVT_OPS_SURVEY_COMPLETED | EVT_TRX_SITE_SURVEY_COMPLETED |
| EVT_OPS_SURVEY_STARTED | EVT_TRX_SITE_SURVEY_STARTED |

## A3.5 Quarantine / Reject Rules

| rule_code | when | action | owner | notes |
|---|---|---|---|---|
| SCHEMA_INVALID | payload thiếu field bắt buộc / sai kiểu dữ liệu | QUARANTINE | Data Lead | Không cho vào KPI; cần reconcile. |
| UNAUTHORIZED_ROLE | actor_role không nằm trong actor_roles của event | REJECT | Field Runner | Chặn gian lận. |
| EVIDENCE_MISSING | event yêu cầu evidence nhưng evidence_pack_uri rỗng | REJECT (monetary) / QUARANTINE (non-monetary) | Field Runner | No Evidence - No Pay. |
| EVIDENCE_HASH_FAIL | hash evidence không khớp / integrity fail | REJECT | Data Lead | Bad Evidence - No Pay. |
| IDEMPOTENCY_DUP | idempotency_key trùng trong window | IGNORE_DUPLICATE | System | Idempotency đảm bảo đúng 1 lần. |
| TIMESTAMP_FUTURE | event_at > now + skew_allowance | QUARANTINE | Data Lead | Tránh fake time. |
| STATE_DRIFT | from_state không khớp trạng thái hiện tại | QUARANTINE | Data Lead | Cần reconcile trước khi apply. |
| PII_NO_CONSENT | payload chứa PII nhưng chưa có consent hợp lệ | REDACT + QUARANTINE | Data Lead | Không lưu PII khi chưa consent (P0.1). |

## A3.6 Event → State mapping table

| event_code | from | to | category | monetary_impact |
|---|---|---|---|---|
| EVT_DISC_DRONE_SCAN_CREATED | NULL | SHADOW | discovery | NO |
| EVT_DISC_LEGACY_IMPORT_CREATED | NULL | SHADOW | discovery | NO |
| EVT_VER_HOUSE_QUALIFIED | SHADOW | QUALIFIED | verification | NO |
| EVT_VER_CONSENT_OTP_VERIFIED | QUALIFIED | CLAIMED | verification | NO |
| EVT_VER_CONSENT_REVOKED | CLAIMED | QUALIFIED | verification | NO |
| EVT_FIN_CASH_COLLECTED | CLAIMED | FINANCIAL | financial | YES |
| EVT_DISC_VDCD_PACK_CREATED | SHADOW | SHADOW | discovery | NO |
| EVT_VER_VDCD_QA_PASSED | SHADOW | SHADOW | verification | NO |
| EVT_DISC_VDCD_API_PUBLISHED | SHADOW | SHADOW | discovery | NO |
| EVT_HOUSE_BUILT_YEAR_SET | NULL | None | house_profile | NO |
| EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_SET | NULL | None | house_profile | NO |
| EVT_HOUSE_EXPECTED_COMPLETION_SET | NULL | None | house_profile | NO |
| EVT_HOUSE_TAG_ADDED | NULL | None | tagging | NO |

## A3.7 Event Catalog (tóm tắt)

| event_code | name_vi | category | entity_scope | monetary_impact | evidence_required | idempotency_key_fields |
|---|---|---|---|---|---|---|
| EVT_DISC_DRONE_SCAN_CREATED | Drone tạo bản quét mái/nhà | discovery | house | NO | EV_TIME, EV_ACTOR, EV_GEO, EV_PHOTO_EXIF, EV_LINK | source_batch_id, house_id |
| EVT_DISC_LEGACY_IMPORT_CREATED | Import dữ liệu cũ (legacy) vào House_ID | discovery | house | NO | EV_TIME, EV_ACTOR, EV_LINK | legacy_source, legacy_record_id |
| EVT_DISC_CLUSTER_ASSIGNED | Gán nhà vào cụm địa lý (cluster) để mô phỏng lan truyền | discovery | house | NO | EV_TIME, EV_ACTOR, EV_LINK | cluster_id, house_id, cluster_method |
| EVT_ENG_UST_CHECKIN | UST check-in tại nhà (tiếp cận) | engagement | house | NO | EV_TIME, EV_ACTOR, EV_GEO, EV_PHOTO_EXIF, EV_LINK | actor_id, house_id, event_at |
| EVT_ENG_ADGPRO_CHECKIN | ADG Pro check-in khảo sát/thi công tại nhà | engagement | house | NO | EV_TIME, EV_ACTOR, EV_GEO, EV_PHOTO_EXIF, EV_LINK | actor_id, house_id, purpose, event_at |
| EVT_ENG_REFERRAL_CREATED | Tạo referral/giới thiệu (người giới thiệu đem lead về) | engagement | lead | NO | EV_TIME, EV_ACTOR, EV_LINK | referrer_id, channel, lead_id |
| EVT_ENG_LEAD_CREATED | Tạo lead (nhu cầu) gắn House_ID nếu có | engagement | lead | NO | EV_TIME, EV_ACTOR, EV_LINK | lead_id |
| EVT_ENG_FREE_SERVICE_GRANTED | Cấp dịch vụ miễn phí (quà tặng) cho dân/chính quyền | engagement | house | NO | EV_TIME, EV_ACTOR, EV_LINK | beneficiary_type, gift_code, house_id |
| EVT_VER_HOUSE_QUALIFIED | Nhà được qualify (đủ điều kiện bước đầu) bởi UST/Runner | verification | house | NO | EV_TIME, EV_ACTOR, EV_LINK | house_id, actor_id, event_at |
| EVT_VER_CONSENT_REQUESTED | Gửi yêu cầu consent (đồng ý) tới chủ nhà | verification | house | NO | EV_TIME, EV_ACTOR, EV_LINK | consent_request_id |
| EVT_VER_CONSENT_OTP_VERIFIED | Consent được xác nhận (OTP verified) – cho phép lưu PII | verification | house | NO | EV_TIME, EV_ACTOR, EV_LINK, EV_CONSENT_OTP | consent_id |
| EVT_VER_CONSENT_REVOKED | Chủ nhà rút consent (revoked) – kích hoạt policy xóa/ẩn PII | verification | house | NO | EV_TIME, EV_ACTOR, EV_LINK | consent_id, house_id |
| EVT_VER_EVIDENCE_PACK_SUBMITTED | Nộp evidence pack (bộ bằng chứng số) cho một bước nghiệp vụ | verification | house | NO | EV_TIME, EV_ACTOR, EV_LINK, EV_PHOTO_EXIF | evidence_pack_uri |
| EVT_VER_EVIDENCE_PACK_VALIDATED | Hệ thống chấm evidence pack (pass/fail, score) | verification | house | NO | EV_TIME, EV_ACTOR, EV_LINK | evidence_pack_uri, pass_flag |
| EVT_TRX_SITE_SURVEY_STARTED | Bắt đầu khảo sát tại nhà (Survey Started) | transaction | lead+house | NO | geo_checkin, photo_site | house_id, lead_id, started_at |
| EVT_OPS_REWORK_OPENED | Mở việc làm lại (Rework Opened) | transaction | job+house | NO | photo_issue, geo_checkin | job_id, opened_at, rework_reason_code |
| EVT_TRX_SITE_SURVEY_COMPLETED | Khảo sát hoàn tất (đo đạc, tính toán) – chuẩn bị báo giá | transaction | job | NO | EV_TIME, EV_ACTOR, EV_GEO, EV_LINK, EV_PHOTO_EXIF | job_id, survey_report_uri |
| EVT_TRX_CPQ_QUOTE_CREATED | Tạo báo giá CPQ (Configure-Price-Quote | cấu hình-giá-báo giá) | transaction | job | NO | EV_TIME, EV_ACTOR, EV_LINK | cpq_quote_id |
| EVT_TRX_ORDER_SIGNED | Chốt hợp đồng/đơn hàng (ký) | transaction | job | NO | EV_TIME, EV_ACTOR, EV_LINK, EV_DOC_SIGN | contract_id |
| EVT_TRX_JOB_STARTED | Bắt đầu thi công | transaction | job | NO | EV_TIME, EV_ACTOR, EV_GEO, EV_PHOTO_EXIF, EV_LINK | job_id, event_at, installer_role |
| EVT_TRX_INSTALL_COMPLETED | Hoàn tất lắp đặt | transaction | job | NO | EV_TIME, EV_ACTOR, EV_GEO, EV_BEFORE_AFTER, EV_LINK | job_id, completion_photo_uri |
| EVT_TRX_QA_PASSED | QA đạt (kiểm tra chất lượng qua checklist) | transaction | job | NO | EV_TIME, EV_ACTOR, EV_LINK, EV_QA_CHECKLIST | qa_checklist_id, pass_flag |
| EVT_TRX_HANDOVER_SIGNED | Bàn giao/ nghiệm thu ký | transaction | job | NO | EV_TIME, EV_ACTOR, EV_LINK, EV_DOC_SIGN, EV_BEFORE_AFTER | handover_doc_id |
| EVT_FIN_CASH_COLLECTED | Thu tiền (tiền thật đã về) – kích hoạt split engine | financial | payment | YES | EV_TIME, EV_ACTOR, EV_LINK, EV_TXN_PROOF | idempotency_key |
| EVT_FIN_SPLIT_ALLOCATED | Hệ thống tạo bảng phân bổ (allocation) theo split rule | financial | payment | YES | EV_TIME, EV_ACTOR, EV_LINK | txn_id, split_rule_ref |
| EVT_FIN_PAYOUT_SENT | Chi trả thưởng/chi phí ra ví (payout sent) | financial | payment | YES | EV_TIME, EV_ACTOR, EV_LINK, EV_TXN_PROOF | payout_id |
| EVT_FIN_RECONCILED | Đối soát ledger (reconciled) – khóa sổ | financial | payment | YES | EV_TIME, EV_ACTOR, EV_LINK, EV_RECONCILE | reconcile_id |
| EVT_ENG_NEIGHBOR_INFLUENCE_EMITTED | Hệ thống phát tín hiệu lan truyền sang hàng xóm sau khi có job thành công | engagement | house | NO | EV_TIME, EV_ACTOR, EV_LINK | source_house_id, cluster_id, event_at |
| EVT_FIN_INVOICE_ISSUED | Phát hành hóa đơn VAT (Invoice issued) | financial | job | YES | EV_TIME, EV_ACTOR, EV_LINK, EV_TXN_PROOF | invoice_id |
| EVT_FIN_VAT_REMITTED | Nộp VAT (VAT remitted) vào ngân sách | financial | payment | YES | EV_TIME, EV_ACTOR, EV_TXN_PROOF, EV_RECONCILE | vat_payment_id |
| EVT_DISC_VDCD_PACK_CREATED | Tạo gói VDCD House_ID (2D/3D/GeoJSON/API) cho nhà | discovery | house | NO | EV_TIME, EV_ACTOR, EV_LINK, EV_QA_CHECKLIST | vdcd_pack_id, house_id, artifact_hash_sha256 |
| EVT_VER_VDCD_QA_PASSED | QA gói VDCD đạt (pass) cho nhà | verification | house | NO | EV_TIME, EV_ACTOR, EV_LINK, EV_QA_CHECKLIST | vdcd_pack_id, artifact_hash_sha256 |
| EVT_DISC_VDCD_API_PUBLISHED | Publish API/GeoJSON cho gói VDCD | discovery | house | NO | EV_TIME, EV_ACTOR, EV_LINK | vdcd_pack_id, api_version, checksum_sha256 |
| EVT_FIN_PILOT_BUDGET_SET | Chốt ngân sách pilot (CAPEX/OPEX/Buffer) | financial | pilot | NO | EV_TIME, EV_ACTOR, EV_DOC_SIGN | pilot_id, commune_id, effective_from |
| EVT_FIN_CAPEX_COMMITTED | Ghi nhận cam kết CAPEX (thiết bị/nền tảng/đầu tư ban đầu) | financial | pilot | NO | EV_TIME, EV_ACTOR, EV_DOC_SIGN | capex_item_code, amount_vnd, committed_at |
| EVT_FIN_OPEX_INCURRED | Ghi nhận OPEX (chi phí vận hành/marketing) phát sinh | financial | pilot | NO | EV_TIME, EV_ACTOR, EV_TXN_PROOF | cost_center, amount_vnd, incurred_at |
| EVT_ENG_ROSTER_CORE_LOCKED | Khóa roster core team (Field Runner/UST/ADG Pro/EPC/Clerk) | engagement | pilot | NO | EV_TIME, EV_ACTOR, EV_LINK | pilot_id, commune_id, roster_version |
| EVT_ENG_ROLE_ASSIGNED | Gán vai trò cho user nội bộ (không PII) | engagement | roster | NO | EV_TIME, EV_ACTOR, EV_LINK | user_id, role_code, start_at |
| EVT_ENG_CAPACITY_SET | Chốt năng lực chịu tải theo vai trò (capacity) | engagement | pilot | NO | EV_TIME, EV_ACTOR, EV_LINK | capacity_model_code, effective_from |
| EVT_HOUSE_BUILT_YEAR_SET | Ghi nhận năm xây dựng nhà (built_year) | house_profile | house | NO | EV_TIME, EV_ACTOR, EV_LINK | house_id, built_year |
| EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_SET | Ghi nhận năm cải tạo lớn gần nhất | house_profile | house | NO | EV_TIME, EV_ACTOR, EV_LINK | house_id, renovation_year |
| EVT_HOUSE_EXPECTED_COMPLETION_SET | Ghi nhận ngày dự kiến hoàn thiện (nhà đang xây) | house_profile | house | NO | EV_TIME, EV_ACTOR, EV_LINK | house_id, expected_completion_date |
| EVT_HOUSE_TAG_ADDED | Thêm tag cho House_ID | tagging | house | NO | EV_TIME, EV_ACTOR | house_id, tag_code, tag_value |

## A3.8 Tích hợp P0-AGE & NewBuild

- Age events: EVT_HOUSE_BUILT_YEAR_SET, EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_SET
- NewBuild events: EVT_HOUSE_EXPECTED_COMPLETION_SET, EVT_HOUSE_TAG_ADDED

## A3.9 Mix vào Appendix (hướng dẫn)

Giữ nguyên A3 gốc (bằng chứng). Thêm file overlay canonical này vào Appendix/A3. Registry YAML đi kèm copy vào thư mục registry/ để OK Computer đọc.