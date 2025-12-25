**P0.1 — MASTER DATA DICTIONARY + NAMING CONTRACT (KHẮC BIA)**

*Pilot D2Com Yên Lạc — Bản chuẩn hoá V5.0.1 (bổ sung governance + time +
finance lineage)*

*D-Day: 01/04/2026 \| Patch date: 24/12/2025 \| P0.1 build: 24/12/2025*

Mục tiêu: khoá chuẩn dữ liệu để người đọc hiểu, audit được, và AI/OK
Computer bóc ra registry + code chạy đúng (không phải đoán).

Chốt quyết định P0 (đã khoá):

1\) house_lifecycle_status canonical dùng ENUM UPPERCASE
(SHADOW→QUALIFIED→CLAIMED→FINANCIAL→GOLDEN).

2\) data_verify_level và verification_level_v2 là 2 biến KHÁC nghĩa
(không gộp).

3\) construction_stage, expected_completion_date, unit_id là BẮT BUỘC
trong pilot (không được thiếu).

Bổ sung P0.1 (vì phản biện đúng các điểm gãy):

\- Alias Governance: ai được thêm alias, sunset, lint chống vòng, audit
định kỳ.

\- Tiered Kill-switch: 3 tầng Warning/Throttle/Hard Stop (khoá trigger +
action + owner + rollback).

\- Business Calendar: khoá quy tắc tính SLA/latency theo giờ-ngày nghiệp
vụ.

\- Finance Lineage Minimum: khoá phụ thuộc downstream để tránh ‘đổi 1 số
gãy cả chuỗi’.

\- 3 bổ sung hardening: Chain-of-custody evidence, Consent snapshot cho
financial event, Quarantine budget.

# 1. Mục tiêu P0.1 và cách dùng

P0.1 là bản mở rộng của P0: giữ nguyên nội dung P0, chỉ thêm luật quản
trị và ngữ nghĩa thời gian/tài chính để tránh drift và tránh simulator
báo sai.

Nguyên tắc: append-only (chỉ ghi thêm). Không ai được ‘sửa lịch sử’ bằng
cách edit record cũ.

# 2. Thuật ngữ (English → Tiếng Việt) và ví dụ

| Thuật ngữ (EN)                | Dịch nghĩa (VI)              | Giải thích ngắn                                  | Ví dụ cụ thể                                         |
|-------------------------------|------------------------------|--------------------------------------------------|------------------------------------------------------|
| SSOT (Single Source of Truth) | Một nguồn sự thật            | Chuẩn cuối chỉ nằm 1 chỗ                         | house_lifecycle_status chỉ định nghĩa 1 nơi.         |
| Canonical                     | Chuẩn gốc                    | Tên/giá trị chuẩn mà code dùng                   | EVT_HOUSE_CREATED là chuẩn; HOUSE_CREATED là alias.  |
| Alias Map                     | Bảng ánh xạ tên cũ→tên chuẩn | Giữ tương thích lịch sử nhưng chống drift        | shadow→SHADOW.                                       |
| Governance                    | Cơ chế quản trị              | Ai có quyền sửa/thêm + luật audit                | Alias chỉ Data Lead được thêm.                       |
| Sunset Date                   | Ngày hết hạn                 | Ngày alias bị ngừng dùng                         | Alias migration tối đa 90 ngày.                      |
| Linter                        | Bộ kiểm quy tắc              | Tự động bắt lỗi cấu hình                         | Chặn alias trỏ vòng (circular).                      |
| Append-only                   | Chỉ ghi thêm                 | Cấm sửa/xoá lịch sử                              | Đổi expected_completion_date phải tạo event UPDATED. |
| Tier (Kill-switch tier)       | Tầng cầu dao                 | Cấp phản ứng rủi ro                              | Tier-1 cảnh báo; Tier-3 dừng hẳn.                    |
| Throttle                      | Hãm tải                      | Giảm nhịp hệ thống thay vì dừng                  | Tạm ngừng phân lead mới.                             |
| Hard Stop                     | Dừng khẩn                    | Ngắt payout/đóng pilot khi vượt ngưỡng đỏ        | Disable payout API.                                  |
| Business Calendar             | Lịch nghiệp vụ               | Quy tắc giờ/ngày làm việc để tính SLA            | Cuối tuần không tính SLA.                            |
| Temporal Paradox              | Nghịch lý thời gian          | SLA tính 24h nhưng thực tế 3 ngày do nghỉ        | Survey_lead_time_hours bị ảo.                        |
| Lineage                       | Dòng phụ thuộc               | Đổi input nào kéo theo output nào                | discount_rate đổi → margin đổi → split đổi.          |
| Event Ledger                  | Sổ cái sự kiện               | Nguồn tính KPI/chi trả                           | Payout chỉ dựa event PASS + evidence.                |
| Schema Validation             | Kiểm định cấu trúc           | Sai schema thì quarantine/reject                 | Thiếu house_id → QUARANTINE.                         |
| Quarantine                    | Cách ly dữ liệu lỗi          | Không tính KPI/payout cho tới khi xử lý          | Event FAIL nằm trong quarantine queue.               |
| Chain of Custody              | Chuỗi lưu giữ bằng chứng     | Dấu vết ai/thiết bị/phiên bản tạo evidence       | capture_device_id + app_version.                     |
| Consent Snapshot              | Ảnh chụp trạng thái đồng ý   | Trạng thái consent tại thời điểm event tài chính | consent_status_at_event=CONSENTED.                   |

Cách đọc nhanh:

\- Mỗi thuật ngữ EN xuất hiện lần đầu phải kèm bản dịch VI và ví dụ.

\- Code dùng canonical; alias chỉ là cầu nối ingest.

Lỗi hay gặp:

\- Dùng thuật ngữ EN mà không định nghĩa (người đọc hiểu sai).

\- Đặt 2 canonical cho cùng một ý (đứt SSOT).

# 3. Priority of Truth (Thứ tự nguồn đúng)

1\) P0.1 Khắc bia (pilot) — chuẩn vận hành & triển khai.

2\) Data Dictionary v2 (toàn dự án) — superset để mở rộng.

3\) Appendix (bản gốc) — bằng chứng tham chiếu. Nếu mâu thuẫn, ưu tiên
(1) rồi (2).

# 4. ID Spine — Trục định danh lõi

| Thực thể | Field canonical | Định nghĩa (thuần Việt)                            | Kiểu   | Phân loại  | Ví dụ                  |
|----------|-----------------|----------------------------------------------------|--------|------------|------------------------|
| Nhà      | house_id        | Mã nhà duy nhất (01 nhà thực tế = 01 house_id).    | string | Non-PII    | house_id=YL-001-000123 |
| Thửa đất | parcel_id       | Mã thửa đất (liên kết nhiều nhà nếu cần).          | string | Non-PII    | parcel_id=PAR-000045   |
| Mái      | roof_id         | Mã mái (1 nhà có thể nhiều mái).                   | string | Non-PII    | roof_id=ROOF-02        |
| Tài sản  | asset_id        | Mã tài sản gắn nhà (solar/cửa/tủ bếp...).          | string | Non-PII    | asset_id=SOLAR-INV-01  |
| Đơn vị ở | unit_id         | Mã đơn vị ở (nếu 1 nhà nhiều căn). BẮT BUỘC pilot. | string | Non-PII    | unit_id=U01            |
| Job      | job_id          | Mã công việc (khảo sát/lắp đặt/bảo hành...).       | string | Restricted | job_id=JOB-2026-0009   |

# 5. Canonical State Machine — house_lifecycle_status (UPPERCASE)

| State (EN) | Trạng thái (VI)   | Điều kiện vào                         | Điều kiện ra                                    | Ví dụ                  |
|------------|-------------------|---------------------------------------|-------------------------------------------------|------------------------|
| SHADOW     | Nhà ‘bóng’        | Có tọa độ/địa chỉ tối thiểu           | Đủ dữ liệu để QUALIFIED                         | Nhà vừa ghi nhận UAV   |
| QUALIFIED  | Đủ chuẩn dữ liệu  | Polygon mái hợp lệ + verify tối thiểu | Được CLAIMED                                    | Có polygon + ảnh       |
| CLAIMED    | Đã nhận xử lý     | UST/Runner/ADGPro claim               | Sang FINANCIAL khi đủ điều kiện                 | UST claim để tư vấn    |
| FINANCIAL  | Vào lớp tài chính | Có hợp đồng/đơn hàng/thu tiền         | Sang GOLDEN khi đối soát xong                   | Đã thu cọc             |
| GOLDEN     | Dữ liệu vàng      | Sạch + consent đúng + evidence đủ     | Không ‘ra’ (chỉ RETIRED/MERGED ở record_status) | Nhà hoàn tất & ổn định |

## 5.1 house_record_status (bổ sung để không phá 5-state)

| Field               | Giải thích                            | Enum                        | Ví dụ  | Ghi chú                     |
|---------------------|---------------------------------------|-----------------------------|--------|-----------------------------|
| house_record_status | Trạng thái hồ sơ nhà (khác lifecycle) | ACTIVE/MERGED/RETIRED/SPLIT | MERGED | Dùng cho dedup/merge/split. |

# 6. Verification — 2 biến khác nghĩa: data_verify_level vs verification_level_v2

| Field                 | Giải thích (thuần Việt)                                                      | Kiểu     | Dùng để làm gì                             | Ví dụ                                         |
|-----------------------|------------------------------------------------------------------------------|----------|--------------------------------------------|-----------------------------------------------|
| data_verify_level     | Độ tin cậy dữ liệu (L0..L5) dựa trên chất lượng evidence & kiểm tra dữ liệu. | int      | Chống garbage data, đo chất lượng dữ liệu. | L3 = polygon + ảnh + đối soát địa danh        |
| verification_level_v2 | Mức xác thực chuẩn v2 (L0..L5) dùng cho KPI & payout.                        | enum/int | Điều kiện tính KPI/chi trả; audit.         | L4 = schema PASS + actor hợp lệ + evidence đủ |

# 7. New Build (nhà đang xây) — BẮT BUỘC trong pilot

Gốc từ Data Dictionary v2 (toàn dự án):

| Field                    | Định nghĩa (gốc v2)                                         | Kiểu   | Phân loại | Ghi chú                                         |
|--------------------------|-------------------------------------------------------------|--------|-----------|-------------------------------------------------|
| construction_stage       | Giai đoạn xây dựng: foundation/frame/rough/finish/occupied. | enum   | Non-PII   | \[NEW v2\] Cốt lõi khai thác phân khúc nhà mới. |
| expected_completion_date | Ngày dự kiến hoàn thiện nhà.                                | date   | Non-PII   | \[NEW v2\] Dùng dự báo nhu cầu bếp/cửa/solar.   |
| unit_id                  | Mã đơn vị ở (nếu 1 nhà nhiều căn/đơn vị).                   | string | Non-PII   | \[NEW v2\] Dùng chống đếm sai khi split.        |

Chuẩn pilot V5.0.1 (khóa):

| Field canonical          | Quy tắc bắt buộc                                       | Nguồn cập nhật (append-only)             | Ví dụ      |
|--------------------------|--------------------------------------------------------|------------------------------------------|------------|
| construction_stage       | Bắt buộc; enum: FOUNDATION/FRAME/ROUGH/FINISH/OCCUPIED | EVT_CONSTRUCTION_STAGE_SET/UPDATED       | ROUGH      |
| expected_completion_date | Bắt buộc; định dạng YYYY-MM-DD                         | EVT_EXPECTED_COMPLETION_DATE_SET/UPDATED | 2026-06-15 |
| unit_id                  | Bắt buộc; nếu 1 nhà 1 căn dùng U01 mặc định            | Master/Survey + snapshot từ event        | U01        |

## 7.1 Tag nghiệp vụ: NewBuild_Candidate / NewBuild_Confirmed (qua event ledger)

| Tag                | Ý nghĩa                               | Bằng chứng tối thiểu                    | Expiry  | Ví dụ            |
|--------------------|---------------------------------------|-----------------------------------------|---------|------------------|
| NewBuild_Candidate | Ứng viên nhà đang/chuẩn bị xây        | Ảnh hiện trường hoặc xác nhận xã        | 30 ngày | Nhà vừa đổ móng  |
| NewBuild_Confirmed | Xác nhận nhà đang xây (đủ độ tin cậy) | Ảnh + vị trí + actor hợp lệ + hash PASS | 45 ngày | Nhà đang xây thô |

## 7.2 Mapping từ tag build-stage (pilot gốc) → construction_stage (pilot V5.0.1)

| Tag pilot gốc            | Derived house_build_stage | Map gợi ý (coarse)     | Cần data bổ sung để fine-stage                 | Ví dụ            |
|--------------------------|---------------------------|------------------------|------------------------------------------------|------------------|
| stage_pre_build          | pre_build                 | FOUNDATION (hoặc NULL) | Cần evidence xác nhận                          | Nhà chuẩn bị xây |
| stage_under_construction | under_construction        | ROUGH (default)        | Có ảnh/video để refine FOUNDATION/FRAME/FINISH | Nhà đang xây     |
| stage_renovating         | renovating                | FINISH (tuỳ)           | Cần phân biệt sửa nhỏ vs cải tạo lớn           | Nhà cải tạo      |

# 8. Event Ledger Schema V5.0.1 (append-only) — khoá chống rác/giả

Gốc pilot (trích schema hiện có):

| Cột                       | TECH_NAME         | Kiểu dữ liệu | Ghi chú                                              |
|---------------------------|-------------------|--------------|------------------------------------------------------|
| ID sự kiện                | event_log_id      | uuid         | Khóa chính event                                     |
| Khóa nhà                  | house_id          | string       | Bắt buộc                                             |
| Khóa job                  | job_id            | string       | Nếu event gắn job                                    |
| Loại sự kiện              | event_type        | string/enum  | Ví dụ: CASH_COLLECTED, CONSENT_REVOKED               |
| Thời điểm                 | event_at          | datetime     | UTC hoặc Asia/Ho_Chi_Minh (khóa timezone thống nhất) |
| Vai trò thực hiện         | actor_role        | string/enum  | ust/adgpro/field_runner/system                       |
| Định danh người thực hiện | actor_id          | string       | party_id hoặc id nội bộ                              |
| Bằng chứng                | evidence_pack_uri | string       | Thiếu evidence thì không pass gate                   |
| Payload mở rộng           | payload_json      | json         | Dữ liệu phụ trợ, không dùng làm khóa                 |

Bổ sung bắt buộc V5 (P0) — đã có: idempotency_key,
schema_validation_status, evidence_integrity_hash, event_code.

Bổ sung bắt buộc V5.0.1 (P0.1) — ADD: chain-of-custody + consent
snapshot + quarantine budget fields:

| Nhóm              | TECH_NAME               | Kiểu     | Mục tiêu                                      | Ví dụ                     |
|-------------------|-------------------------|----------|-----------------------------------------------|---------------------------|
| Chain-of-custody  | evidence_captured_at    | datetime | Ghi thời điểm tạo evidence (chống ‘nộp muộn’) | 2026-03-01T09:10:00+07:00 |
| Chain-of-custody  | capture_device_id       | string   | Dấu vết thiết bị chụp                         | DEV-UST-0007              |
| Chain-of-custody  | capture_app_version     | string   | Dấu vết phiên bản app                         | oneapp-1.3.2              |
| Chain-of-custody  | gps_source              | enum     | Nguồn GPS: GNSS/NETWORK/MANUAL                | GNSS                      |
| Chain-of-custody  | evidence_signature      | string   | Chữ ký số (nếu có)                            | sig:...                   |
| Consent snapshot  | consent_snapshot_id     | string   | Trỏ bản ghi consent tại thời điểm event       | CNS-2026-00012            |
| Consent snapshot  | consent_status_at_event | enum     | CONSENTED/PENDING/REVOKED                     | CONSENTED                 |
| Quarantine budget | quarantine_reason_code  | string   | Lý do cách ly để audit                        | SCHEMA_FAIL               |
| Quarantine budget | quarantine_ttl_days     | int      | Hạn lưu cách ly, quá hạn auto purge           | 14                        |
| Quarantine budget | quarantine_queue_bucket | enum     | SCHEMA/EVIDENCE/ACTOR/FINANCE                 | EVIDENCE                  |

Cách đọc nhanh:

\- No/Bad Evidence - No Pay: hash fail hoặc signature fail là không
payout.

\- Financial event phải có consent snapshot để tránh ‘thu hồi consent
nhưng vẫn trả tiền’.

\- Quarantine phải có reason_code + TTL để không tắc queue.

Lỗi hay gặp:

\- Chỉ kiểm ‘có evidence’ mà không kiểm ‘evidence bị sửa’.

\- Không lưu consent snapshot khiến legal crisis (PII) lây sang finance.

# 9. Alias Map & Governance (chống drift tên)

9.1 Alias map gốc pilot (trích):

| Tên cũ                  | TECH_NAME (canonical)            | Ghi chú              |
|-------------------------|----------------------------------|----------------------|
| House_ID                | house_id                         | Chuẩn hóa chữ thường |
| House_Lifecycle_Status  | house_lifecycle_status           |                      |
| House_Tag_List          | house_tag_list_json              | Đổi sang JSON list   |
| Data_Verify_Level       | data_verify_level                |                      |
| Event_Log_ID            | event_log_id                     |                      |
| Fin_DSO_Days            | fin_dso_days                     |                      |
| Ops_Manual_Entry_Flag   | ops_manual_fallback_flag         |                      |
| Ops_Data_Latency_Hours  | ops_fallback_entry_latency_hours |                      |
| Risk_Img_Metadata_Valid | risk_img_metadata_valid_flag     |                      |

9.2 Alias map bổ sung V5 (ADD):

| Nguồn/Tên cũ                         | Canonical                          | Rule                                  | Ví dụ         |
|--------------------------------------|------------------------------------|---------------------------------------|---------------|
| shadow (lowercase)                   | SHADOW                             | UPPERCASE normalize                   | shadow→SHADOW |
| qualified                            | QUALIFIED                          | UPPERCASE normalize                   |               |
| CASH_COLLECTED (event_type)          | EVT_CASH_COLLECTED (event_code)    | Prefix EVT\_ + alias                  |               |
| HOUSE_CREATED                        | EVT_HOUSE_CREATED                  | Prefix EVT\_ + alias                  |               |
| house_build_stage=under_construction | construction_stage=ROUGH (default) | Coarse default + refine bằng evidence |               |

## 9.3 Alias Governance Rules (bắt buộc)

| Quy tắc         | Nội dung                                                           | Ví dụ                                    |
|-----------------|--------------------------------------------------------------------|------------------------------------------|
| Rule            | Nội dung luật (thuần Việt)                                         | Ví dụ                                    |
| Owner duy nhất  | Mỗi alias chỉ có 1 owner (Data Lead/ Data Team) được phép tạo/sửa. | UST không được tự thêm alias.            |
| Sunset bắt buộc | Alias phải có sunset_date; alias migration tối đa 90 ngày.         | HOUSE_CREATED alias hết hạn sau 90 ngày. |
| No circular     | Alias không được trỏ vào alias khác (chống vòng).                  | A→B (alias) là cấm; phải A→canonical.    |
| Monthly audit   | Mỗi tháng audit, retire alias không dùng \>60 ngày.                | Alias không dùng thì dọn.                |
| Deprecation log | Alias bị deprecate phải log và thông báo.                          | fin_dso_days deprecate, log 90 ngày.     |

## 9.4 Alias Linter Spec (bộ kiểm quy tắc)

\# Alias Linter (pseudo-YAML)  
alias_linter_rules:  
- canonical_must_exist: true  
- no_circular_reference: true  
- alias_to_alias_disallowed: true  
- one_alias_one_canonical: true  
- require_owner_role: true  
- require_sunset_date: true  
- max_sunset_days_migration: 90  
- monthly_audit_required: true

# 10. Quy tắc kiểm định, ngữ nghĩa thời gian, và kill-switch (P0.1 bổ sung)

10.1 Schema Validation: payload sai schema → QUARANTINE (không tính
KPI/payout).

10.2 Actor Validity: actor_id/role phải match HR roster ACTIVE tại
event_at.

10.3 Evidence Integrity: hash mismatch → FAIL (No/Bad Evidence - No
Pay).

10.4 Dedupe: idempotency_key trùng → reject event trùng, giữ 1 bản
canonical.

## 10.5 Tiered Kill-switch (3 tầng: Warning / Throttle / Hard Stop)

\# Kill-switch tiers (example)  
kill_switch_tiers:  
tier_1\_warning:  
trigger: "payload_schema_reject_rate_pct \> 2 for 60m"  
action: "Alert Risk Lead + Data Lead; tăng sample audit evidence"  
owner: "Head of Risk"  
rollback: "rate \< 2 for 24h"  
tier_2\_throttle:  
trigger: "fake_evidence_rate_pct \> 5 for 30m"  
action: "Pause new lead allocation; quarantine pending payout; nâng
gate"  
owner: "CFO"  
rollback: "rate \< 3 for 24h + post-incident review"  
tier_3\_hard_stop:  
trigger: "unconsented_pii_risk \> 0 OR fake_evidence_rate_pct \> 10 for
15m"  
action: "Disable payout API; freeze pilot; trigger war-room"  
owner: "CEO/Commander"  
rollback: "manual sign-off + remediation complete"

Cách đọc nhanh:

\- Tier-1 là cảnh báo, Tier-2 là hãm tải, Tier-3 là dừng khẩn.

\- Consent-risk (unconsented_pii_risk\>0) là kill cứng (Hard Stop) theo
hiến pháp.

Lỗi hay gặp:

\- Không có rollback condition (kéo cầu dao xong không biết mở thế nào).

\- Dùng tên metric không canonical khiến trigger sai.

## 10.6 Business Calendar Registry (chống ‘temporal paradox’)

\# Business calendar (versioned registry)  
business_calendar_registry:  
calendar_version: "VN_2026_v1"  
timezone: "Asia/Ho_Chi_Minh"  
business_hours: "08:00-18:00"  
business_days: "Mon-Sat"  
holiday_calendar_source: "Vietnam official holidays + local
exceptions"  
sla_clock_rule: "Only count business time"

Ví dụ: survey_lead_time_hours chỉ tính giờ làm việc. Nếu tạo lead lúc T7
17:30 và hoàn tất T2 08:30 thì SLA=1h (không phải 63h).

## 10.7 Finance Lineage Minimum (khoá cascade tối thiểu)

\# Finance lineage (minimum)  
finance_lineage_min:  
discount_rate_pct:  
upstream: \["price_list_vnd"\]  
downstream: \["avg_selling_price_vnd", "l1_margin_vnd",
"split_residual_vnd"\]  
recompute_policy: "recompute all downstream within 1h"  
cache_ttl: "1h"  
dso_days:  
upstream: \["invoice_event", "cash_collection_event"\]  
downstream: \["cash_cycle_days", "runway_days"\]  
recompute_policy: "recompute within 30m"  
cache_ttl: "30m"

Nguyên tắc: thay đổi discount_rate_pct mà không tính lại
split_residual_vnd là lỗi cascade (bị cấm).

## 10.8 Quarantine Budget (chống ‘quarantine overflow’)

\# Quarantine budget & policy  
quarantine_policy:  
queue_limit_events: 5000  
ttl_days_default: 14  
auto_purge: true  
purge_rule: "expired_ttl OR resolved_status"  
reprocess_policy:  
allowed: true  
max_reprocess_attempts: 2  
require_owner_signoff: true

Ví dụ: event QUARANTINE vì SCHEMA_FAIL có TTL 14 ngày. Hết hạn chưa xử
lý thì auto purge (append-only log vẫn giữ).

# 11. Patch Ledger (P0 + P0.1) — tóm tắt để truy vết

| Patch ID | Triệu chứng                  | Root cause                                                | Patch (V5.0.1)                                         | Test nhanh                                |
|----------|------------------------------|-----------------------------------------------------------|--------------------------------------------------------|-------------------------------------------|
| P0-01    | Enum state lệch casing       | shadow vs SHADOW                                          | Normalize UPPERCASE + alias map                        | State_count không tách 2 nhóm             |
| P0-02    | Miss new_build_candidate     | Thiếu construction_stage/expected_completion_date/unit_id | Bổ sung bắt buộc + event set/updated                   | NewBuild count \>0 khi under_construction |
| P0-03    | Event naming drift           | EVENT\_/tên trần                                          | Canonical EVT\_\* + alias map                          | Loader output chỉ EVT\_\*                 |
| P0-04    | Fake/garbage evidence lọt    | Thiếu hash/schema status                                  | Add schema_validation_status + evidence_integrity_hash | Hash fail không payout                    |
| P0-05    | Duplicate payout             | Thiếu idempotency_key                                     | Add idempotency_key                                    | Gửi 2 lần chỉ nhận 1                      |
| P0.1-06  | Alias drift sau 3 tháng      | Thiếu governance                                          | Alias Governance + Linter + sunset                     | Alias circular bị chặn                    |
| P0.1-07  | Kill phản ứng mù             | Thiếu tier + rollback                                     | Tiered kill-switch + owner + rollback                  | Fake_evidence\>10% kích hard stop         |
| P0.1-08  | SLA mô phỏng sai             | Thiếu business calendar                                   | Business calendar registry + SLA clock rule            | SLA theo business-time                    |
| P0.1-09  | Cascade tài chính            | Thiếu lineage                                             | Finance lineage minimum + recompute policy             | Discount đổi -\> split đổi                |
| P0.1-10  | Quarantine overflow          | Không có TTL/limit                                        | Quarantine budget + TTL/purge/reprocess                | Queue không phình vô hạn                  |
| P0.1-11  | Evidence bị ‘mông má’        | Thiếu chain-of-custody                                    | Add captured_at/device/app/gps/signature               | Audit thấy nguồn tạo evidence             |
| P0.1-12  | Consent thu hồi vẫn trả tiền | Thiếu snapshot                                            | Add consent_snapshot_id/status_at_event                | Payout check snapshot                     |

# 12. Appendix — Trích bảng gốc để đối chiếu nhanh (giữ nguyên văn)

## 12.1 Pilot gốc — Core groups (bảng TECH_NAME)

| Nhóm               | TECH_NAME                   | Kiểu dữ liệu             | Ghi chú vận hành                                           |
|--------------------|-----------------------------|--------------------------|------------------------------------------------------------|
| Lifecycle Status   | house_lifecycle_status      | enum                     | Ví dụ: shadow/qualified/claimed/financial/golden           |
| Tag/Profile        | house_tag_list_json         | json (array\[string\])   | Mọi tag phải có expiry_date; tag hết hạn phải tái xác minh |
| Verification Level | data_verify_level           | int                      | Mức tin cậy dữ liệu (L0..L5)                               |
| Event Ledger       | event_log_id / event_ledger | uuid + append-only table | Mọi KPI đếm từ event_ledger (không đếm tay)                |

## 12.2 Pilot gốc — Build-stage tags

| Tag bắt buộc             | Ý nghĩa          | Derived house_build_stage |
|--------------------------|------------------|---------------------------|
| stage_pre_build          | Nhà chuẩn bị xây | pre_build                 |
| stage_under_construction | Nhà đang xây     | under_construction        |
| stage_renovating         | Nhà đang cải tạo | renovating                |

## 12.3 Global v2 — 3 field NEW v2 (nhà đang xây)

| Field                    | Định nghĩa (thuần Việt)                                     | Kiểu   | Phân loại | Ghi chú/Ứng dụng                                |
|--------------------------|-------------------------------------------------------------|--------|-----------|-------------------------------------------------|
| construction_stage       | Giai đoạn xây dựng: foundation/frame/rough/finish/occupied. | enum   | Non-PII   | \[NEW v2\] Cốt lõi khai thác phân khúc nhà mới. |
| expected_completion_date | Ngày dự kiến hoàn thiện nhà.                                | date   | Non-PII   | \[NEW v2\] Dùng dự báo nhu cầu bếp/cửa/solar.   |
| unit_id                  | Mã đơn vị ở (nếu 1 nhà nhiều căn/đơn vị).                   | string | Non-PII   | \[NEW v2\] Dùng chống đếm sai khi split.        |
