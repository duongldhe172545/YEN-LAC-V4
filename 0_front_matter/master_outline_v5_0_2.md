**HIẾN PHÁP D2com - YÊN LẠC (DDAY 01/04/2026)  
MASTER OUTLINE V5 (Skeleton chuẩn hóa)**

Người xây dựng: Nguyễn Quốc Vinh - TP MKT D2com - Tập đoàn Austdoor  
Phiên bản: V5 (khóa khung) \| Bản vá: cập nhật ngày 24/12/2025 \| Phạm
vi: Tập đoàn + Pilot Yên Lạc

Nguyên tắc: tài liệu này là SSOT về cấu trúc (structure). Nội dung triển
khai chi tiết sẽ được “đổ” vào theo append-only: Revision History +
Patch Ledger + Decision Log.

# 0. Front-matter

## 0.1 Trang bìa

Giữ đúng metadata: tên tài liệu, người xây dựng, phiên bản, ngày patch,
phạm vi.  
(DDAY 01/04/2026)

| Người xây dựng       | Nguyễn Quốc Vinh - TP MKT D2com - Tập đoàn Austdoor                 |
|----------------------|---------------------------------------------------------------------|
| Phiên bản            | V5 (Skeleton)                                                       |
| Bản vá cập nhật ngày | 24/12/2025                                                          |
| Phạm vi              | Cấp tập đoàn; dùng cho War-room HĐQT và triển khai Pilot xã Yên Lạc |
| Nguyên tắc SSOT      | SPINE là nguồn sự thật duy nhất; Appendix chỉ làm bằng chứng        |

## 0.2 Revision History (Lịch sử phiên bản)

Bảng mẫu: Revision History

| Version | Ngày hiệu lực | Thay đổi chính                                                              | Tác động                                  | Owner            | Link Patch/Decision               |
|---------|---------------|-----------------------------------------------------------------------------|-------------------------------------------|------------------|-----------------------------------|
| V5      | 24/12/2025    | Bổ sung NewBuild fields + quarantine/evidence integrity + kill-switch tiers | Không đổi SSOT, chỉ bổ sung registry/spec | System Architect | Patch:P0-NEWBUILD; Decision:D-011 |

**Cách đọc nhanh:**

Nhìn cột “Thay đổi chính” để biết bản này thêm gì, cột “Link
Patch/Decision” để truy vết.

**Lỗi hay gặp:**

-   Ghi thay đổi kiểu chung chung (“cập nhật nhiều mục”) dẫn đến audit
    hỏi không trả lời được.

-   Không link Patch/Decision làm mất traceability (truy vết).

## 0.3 Patch Ledger Index (Danh mục bản vá)

Bảng mẫu: Patch Ledger Index

| Patch_ID | Triệu chứng         | Root cause (gốc rễ)         | Patch (vá)                                 | Test                       | Rollback            |
|----------|---------------------|-----------------------------|--------------------------------------------|----------------------------|---------------------|
| P0-02    | VDCD vendor lock-in | Tên field/metric gắn vendor | Chuẩn hóa provider-neutral + provider_code | lint:vdcd_prefix_forbidden | Re-enable alias map |

**Cách đọc nhanh:**

Patch_ID là khóa. Mọi sửa đổi phải có Patch_ID hoặc Decision_ID.

**Lỗi hay gặp:**

-   Sửa lén trong nội dung mà không có Patch_ID (vi phạm append-only).

-   Patch không có test/rollback thì lúc nổ không biết quay lại.

## 0.4 Decision Log Index (Danh mục quyết định)

Bảng mẫu: Decision Log

| Decision_ID | Quyết định                                             | Lý do                          | Ảnh hưởng                                | Ngày       | Owner            |
|-------------|--------------------------------------------------------|--------------------------------|------------------------------------------|------------|------------------|
| D-011       | Thêm tag NewBuild_Confirmed + expected_completion_date | Tránh miss new_build_candidate | Bổ sung event + metric + simulator edges | 24/12/2025 | System Architect |

## 0.5 Glossary (Thuật ngữ + viết tắt)

Quy tắc: lần đầu xuất hiện, ghi theo format: English term (dịch Việt) -
giải thích - ví dụ.

**SSOT (Single Source of Truth) (Một nguồn sự thật duy nhất):** Chỗ duy
nhất được phép định nghĩa cuối cùng.

-   Ví dụ: house_lifecycle_status chỉ định nghĩa ở SPINE 4.1.

**Append-only (Ghi bổ sung, không sửa lịch sử):** Mọi thay đổi là thêm
event/phiên bản mới, không đè bản cũ.

-   Ví dụ: expected_completion_date đổi bằng
    EVT_HOUSE_EXPECTED_COMPLETION_UPDATED.

**Event sourcing (lưu vết sự kiện) (Lưu trạng thái bằng chuỗi sự
kiện):** State là kết quả, Event là nguyên nhân.

-   Ví dụ: EVT_SURVEY_VERIFIED sinh ra chuyển SHADOW→QUALIFIED.

**Idempotency key (khóa chống trùng) (Khóa để event không bị ghi
trùng):** Cùng 1 thao tác, ghi nhiều lần vẫn ra 1 kết quả.

-   Ví dụ: EVT_HANDOVER_SIGNED dùng
    idempotency_key=job_id+handover_hash.

**Quarantine (cách ly dữ liệu) (Đưa event sai schema/evidence vào vùng
cách ly):** Không cho chạy vào KPI/chi trả.

-   Ví dụ: payload_schema_invalid → quarantine_event.

**Schema validation (kiểm schema) (Kiểm payload_json đúng cấu trúc):**
Thiếu field bắt buộc thì reject/quarantine.

-   Ví dụ: roof_polygon invalid → reject.

**Evidence integrity (toàn vẹn bằng chứng) (Kiểm bằng chứng có bị
giả/mạo):** Dùng hash/metadata/timestamp/actor validity.

-   Ví dụ: Ảnh bị sửa GPS metadata → integrity_fail.

**Provider-neutral (Trung tính nhà cung cấp):** Đổi vendor không phải
đổi KPI/field canonical.

-   Ví dụ: vdcd\_\* chỉ nằm provider_raw; canonical là survey\_\*.

**construction_stage (Giai đoạn thi công):** Fine stage:
móng/khung/thô/hoàn thiện/đã ở.

-   Ví dụ: construction_stage=ROUGH (đang xây thô).

**expected_completion_date (Ngày dự kiến hoàn thiện):** Ngày dự kiến bàn
giao/hoàn thiện nhà.

-   Ví dụ: expected_completion_date=2026-05-20.

**NewBuild_Candidate (Ứng viên nhà mới xây):** Tag tạm, chưa xác nhận,
dùng để theo dõi.

-   Ví dụ: EVT_HOUSE_TAG_ADDED tag=NewBuild_Candidate.

**NewBuild_Confirmed (Nhà mới xây đã xác nhận):** Tag đã có evidence,
được phép kích hoạt follow-up.

-   Ví dụ: Tag + evidence_ref=permit_photo.

## 0.6 Registry Map (Bản đồ registry)

Bảng mẫu: Registry Map

| Registry       | Mô tả                        | Định dạng | Owner     | Ví dụ key           | Nằm ở đâu                          |
|----------------|------------------------------|-----------|-----------|---------------------|------------------------------------|
| event_registry | Danh mục event_code + schema | YAML/JSON | Data Lead | EVT_HOUSE_TAG_ADDED | modules/09_taxonomy_event_registry |

**Cách đọc nhanh:**

Muốn code chạy, nhìn Registry Map để biết file cấu hình ở đâu. Tài liệu
chỉ là bản đồ.

**Lỗi hay gặp:**

-   Định nghĩa event/metric ở văn xuôi mà không có registry.

-   Không có owner → không ai chịu trách nhiệm cập nhật.

## 0.7 Governance of Change (Quản trị thay đổi)

Mọi thay đổi registry phải qua quy trình: Lint (kiểm) → Review → Merge →
Version bump (tăng phiên bản).

Bảng mẫu: Deprecation Policy

| Đối tượng   | Trạng thái | Quy tắc               | Ví dụ                   | Thời hạn   |
|-------------|------------|-----------------------|-------------------------|------------|
| metric_code | deprecated | Giữ alias 2 phiên bản | fin_dso_days → dso_days | 2 releases |

# SPINE (XƯƠNG SỐNG: SSOT)

## 1. Scope Lock

1.1 Phạm vi Pilot Yên Lạc  
1.2 Khóa trục KPI: K0–K8 (pilot) + K9 Product Quality + K10 Replication
& Moat  
1.3 In-scope / Out-of-scope

## 2. Nguyên tắc bất biến (Hiến pháp chiến trường)

2.1 Append-only audit  
2.2 No-evidence-no-pay  
2.3 Consent-first PII  
2.4 Kill-switch framework  
2.5 House_ID state machine là KPI lõi

### 2.6 Kill-switch Hierarchy (Bậc thang cầu dao)

Bảng mẫu: Kill-switch Hierarchy

| Level | Tên      | Trigger (khi nào)                | Action (làm gì)                           | Owner    | Ví dụ                    |
|-------|----------|----------------------------------|-------------------------------------------|----------|--------------------------|
| L2    | Throttle | payload_schema_reject_rate \> 5% | Dừng nhận lead mới 24h + audit mẫu 30 job | War-room | Reject spike do nhập tay |

**Cách đọc nhanh:**

Nhìn trigger để biết vì sao bị kéo cầu dao; nhìn action để biết hệ phản
ứng gì.

**Lỗi hay gặp:**

-   Chỉ có “KILL” mà không có mức “Throttle” sẽ làm hệ tắt/mở liên tục.

-   Trigger không ghi đơn vị (%/days/vnd) dễ gây hiểu nhầm.

## 3. Canonical Naming Contract

3.1 snake_case + domain prefix  
3.2 Quy tắc đơn vị: \*\_hours/\*\_days/\*\_vnd/\*\_rate/\*\_pct  
3.3 Provider-neutral naming (VDCD chỉ là dimension provider_code)  
3.4 Alias Registry rule  
3.5 Collision Gate

### 3.6 Provider-neutral Data Model (Trung tính nhà cung cấp)

Bảng mẫu: Provider raw → Canonical mapping

| provider_code | provider_raw_field | canonical_field  | Quy tắc                             | Ví dụ giá trị             |
|---------------|--------------------|------------------|-------------------------------------|---------------------------|
| VDCD          | vdcd_capture_at    | survey_timestamp | ISO datetime, timezone Asia/Bangkok | 2026-03-18T09:12:30+07:00 |

**Cách đọc nhanh:**

Provider raw giữ nguyên để truy vết; canonical dùng để tính KPI và chạy
máy.

**Lỗi hay gặp:**

-   Dùng thẳng vdcd\_\* làm canonical → dính vendor lock-in.

-   Không ghi timezone → SLA/simulator lệch ngày.

## 4. Canonical State Machines

4.1 house_lifecycle_status: SHADOW → QUALIFIED → CLAIMED → FINANCIAL →
GOLDEN  
4.2 Flag/Event tách khỏi state  
4.3 warranty_status tách riêng  
4.4 Idempotency & dedupe rules

### 4.5 Event-to-State Mapping Table (Event là nguyên nhân, State là kết quả)

Bảng mẫu: Event → State transition

| event_code          | from_state | to_state  | Guard conditions (điều kiện)           | Evidence required (bằng chứng) | Failure action   |
|---------------------|------------|-----------|----------------------------------------|--------------------------------|------------------|
| EVT_SURVEY_VERIFIED | SHADOW     | QUALIFIED | roof_polygon_valid=1 & geo_error_m\<10 | img_roof + geojson             | quarantine_event |

**Cách đọc nhanh:**

Đây là bảng dập mọi tranh cãi: event nào mới được phép làm House_ID nhảy
state.

**Lỗi hay gặp:**

-   Trộn VERIFIED/CONSENTED vào state machine 5 trạng thái.

-   Không có guard conditions → dữ liệu rác vẫn đẩy state.

## 5. Data Architecture chuẩn (Data Spine)

5.1 Event Log schema  
5.2 Core Entities  
5.3 Data Contracts  
5.4 Evidence pack + lineage  
5.5 Security & access

### 5.6 Business Calendar & Time Semantics (Lịch nghiệp vụ)

Bảng mẫu: Time semantics

| Khái niệm | Chuẩn                    | Ví dụ               | Tác động                           |
|-----------|--------------------------|---------------------|------------------------------------|
| SLA clock | Chạy theo business hours | 8:00–17:00, nghỉ CN | Tránh báo động giả trong simulator |

## 6. KPI Tree & Param Master (K0–K10)

6.1 K0 Data Spine  
6.2 K1 Lead  
6.3 K2 Ops/Network  
6.4 K3 Sales+Pricing+Financing  
6.5 K4 Cash & Incentive  
6.6 K5 Tech & Adoption  
6.7 K6 Gov/Safety  
6.8 K7 Product Gate  
6.9 K8 Resource/Efficiency  
6.10 K9 Product Quality & Defect  
6.11 K10 Replication & Moat

### 6.12 Principle-to-KPI Trace Matrix (Nguyên tắc → KPI → Event)

Bảng mẫu: Trace Matrix

| Principle          | metric_code                  | event_code(s)         | Evidence             | Owner    | Ví dụ                |
|--------------------|------------------------------|-----------------------|----------------------|----------|----------------------|
| No-evidence-no-pay | evidence_integrity_fail_rate | EVT_EVIDENCE_UPLOADED | hash+timestamp+actor | Ops Lead | Fail \>2% → throttle |

# MODULES (THÂN: VẬN HÀNH + MÁY)

## 7. Runbook vận hành (OKC/On-site)

7.1 Vai trò & RACI  
7.2 Quy trình nạp data & QA  
7.3 Incident playbook  
7.4 Payout & reconcile SOP  
7.5 Evidence Operations Standard

## 8. Pilot Plan & Gate Hardening

8.1 Timeline D-14 → D+90  
8.2 Gate checklist  
8.3 Kill-switch operational  
8.4 Audit evidence requirement  
8.5 Product Quality Gate (K9 Gate)

## 9. Taxonomy & Event Registry

9.1 Event_code canonical (EVT\_\*)  
9.2 Event schema per domain  
9.3 Event alias map  
9.4 Unknown event handling  
9.5 Quarantine & Reconciliation Workflow

### 9.6 NewBuild Events (nhà đang/chuẩn bị xây)

Bảng mẫu: Event schema - NewBuild

| event_code                        | Mục đích                    | Required fields                              | Idempotency key                   | Ví dụ payload                             |
|-----------------------------------|-----------------------------|----------------------------------------------|-----------------------------------|-------------------------------------------|
| EVT_HOUSE_EXPECTED_COMPLETION_SET | Đặt ngày dự kiến hoàn thiện | house_id, expected_completion_date, actor_id | house_id+expected_completion_date | {"expected_completion_date":"2026-05-20"} |

**Cách đọc nhanh:**

NewBuild không đổi state 5 bước, nó đổi “thuộc tính theo thời gian” để
kích follow-up/simulator.

**Lỗi hay gặp:**

-   Nhét NewBuild vào state machine House_ID làm loạn SSOT.

-   Không có idempotency_key → nhập tay nhiều lần sinh drift.

## 10. Metric Registry & Algorithm Specs

10.1 Metric registry structure  
10.2 Algorithm Specs K0–K4  
10.3 Algorithm Specs K5–K8  
10.4 Algorithm Specs K9  
10.5 Algorithm Specs K10  
10.6 Formula registry + unit tests  
10.7 Dependency Graph of Finance & Simulator Params

### 10.8 NewBuild Metrics (bắt ứng viên nhà xây)

Bảng mẫu: Metric spec - NewBuild

| metric_code               | Định nghĩa                            | Grain  | Window | Formula                                      | Ví dụ           |
|---------------------------|---------------------------------------|--------|--------|----------------------------------------------|-----------------|
| new_build_confirmed_count | Số House_ID có tag NewBuild_Confirmed | xa/day | 7d     | count_distinct(house_id where tag=Confirmed) | Yên Lạc: 120/7d |

**Cách đọc nhanh:**

Metric NewBuild dùng để không miss pipeline cho Solar/Tủ bếp, và cho
simulator dự báo nhu cầu theo thời gian.

**Lỗi hay gặp:**

-   Không phân biệt Candidate vs Confirmed → pipeline bị phồng giả.

-   Thiếu window (7d/30d) → số liệu nhảy loạn.

## 11. Thresholds & Kill-switch Rules

11.1 Threshold registry  
11.2 Kill-switch conditions  
11.3 Alerting spec  
11.4 Kill-switch Runbook (Playbook)

### 11.5 Data Quality & Evidence Integrity Kill-switch (dữ liệu rác/bằng chứng giả)

Bảng mẫu: Kill-switch triggers - Data/Evidence

| metric_code                | Yellow | Red   | Level       | Action                            | Ví dụ                          |
|----------------------------|--------|-------|-------------|-----------------------------------|--------------------------------|
| payload_schema_reject_rate | \>=2%  | \>=5% | L2 Throttle | Dừng nhận lead 24h + audit 30 job | Reject tăng do fallback manual |

## 12. Causal Framework & Simulator

12.1 Causal edges registry  
12.2 Stress test scenarios  
12.3 Simulation outputs  
12.4 Time-aware Simulation Rules

### 12.5 NewBuild causal edges (nhà xây → nhu cầu)

Bảng mẫu: Causal edge - NewBuild

| edge_id | from_metric               | to_metric            | lag | sign | confidence | Ví dụ                      |
|---------|---------------------------|----------------------|-----|------|------------|----------------------------|
| E-NB-01 | new_build_confirmed_count | lead_propensity_rate | 14d | \+   | 0.7        | Confirmed ↑ → propensity ↑ |

**Cách đọc nhanh:**

Edge NewBuild giúp simulator dự báo demand theo timeline hoàn thiện nhà,
không dựa cảm giác.

**Lỗi hay gặp:**

-   Không gắn lag/đơn vị thời gian → mô phỏng sai pha.

-   Không gắn confidence → người đọc tưởng chắc như đinh đóng cột.

## 13. Finance & Split Rules

13.1 Finance waterfall & definitions  
13.2 Split rules  
13.3 Reconcile & DSO logic  
13.4 Direct_Cost_per_ID + Yield_per_ID  
13.5 Shadow Pricing → Unit Margin Linkage

## 14. Streamlit / OK Computer Implementation Guide

14.1 Pages map  
14.2 File/Folder conventions + registry loader  
14.3 QA scripts + regression suite  
14.4 Hot reload + release process  
14.5 Registry Linting Rules

# APPENDIX (BẰNG CHỨNG GỐC)

A1–A8. Nguyên văn 8 file (đã clean format)  
A1 Hiến pháp Map Nhân Quả K0–K8  
A2 Kế hoạch Pilot HĐQT  
A3 Taxonomy K0–K8  
A4 Algorithm Specs K0–K4  
A5 Master Data Dictionary “khắc bia”  
A6 Plan MasterData Merged  
A7 Gate checklist hardening  
A8 OKComputer Runbook
