# A2 Overlay - HĐQT Plan (Aligned V5.0.2) - Pilot Yên Lạc

**DDAY (ngày vận hành):** 01/04/2026  
**Ngày cập nhật overlay:** 24/12/2025  
**Nguyên tắc:** append-only (chỉ ghi thêm, không sửa lịch sử); A2 là narrative (kế hoạch cho người đọc), SSOT nằm ở V5 + registry.

## 1. Mục tiêu overlay
Overlay này dùng để liên kết liền mạch A2 (kế hoạch HĐQT) với khung V5/registry đã khóa: Data Dictionary (A5), Event Registry (A3), Algorithm/Metric Registry (A4), Causal Map (A1), Gate Hardening (A7), Runbook (A8). Không thay đổi quyết định LOCKED; chỉ bổ sung bản đồ tham chiếu và alias để tránh drift (lệch chuẩn).

## 2. Drift list cần vá trong A2 để khớp V5.0.2
- Patch naming drift: A2 đang dùng “Integrated Patch v2.0” (P0-03/P0-04/...) khác với Patch Ledger V5.0.2. Cần bảng mapping legacy → canonical.
- State machine drift: A2 nói “House_ID state machine” nhưng chưa chốt ENUM 5 trạng thái UPPERCASE. Cần chèn: SHADOW, QUALIFIED, CLAIMED, FINANCIAL, GOLDEN.
- Event contract drift: A2 chưa ràng buộc event_code chuẩn EVT_* và idempotency_key (khóa chống ghi trùng). Cần dẫn chiếu registry A3.
- Age dimension missing: A2 chưa có trục tuổi nhà (built_year/age_bucket) để phân nhóm hành vi. Cần bổ sung P0-DATA-AGE và event/metric liên quan.
- Go-live hardening: A2 chưa chỉ rõ Unit Test Spec (kiểm thử đơn vị), Rollback (quay lui), Incident SLA (cam kết phản ứng sự cố). Cần dẫn chiếu A8 + patch P0-OPS/P0-QA.
- Metric naming hygiene: một số metric thiếu hậu tố đơn vị/tỉ lệ (_hours/_days/_vnd/_rate/_pct). Cần alias map để code không đoán.

## 3. Bảng mapping Patch legacy (A2) → Patch canonical (V5.0.2)

| Legacy patch code (A2) | Canonical patch (V5.0.2) | Ghi chú |
|---|---|---|
| P0-03 State Violation Silent | P0.2 (A3 Event Registry) + P0.3 (A4 Algorithm Specs) + registry_lints | Chặn nhảy trạng thái im lặng bằng event→state map + lint FATAL. |
| P0-04 Finance Audit & Reconcile Gaps | P0.1 (Khắc bia) + P0-OPS-ROLLBACK + A8 Runbook | Khóa lineage (chuỗi phụ thuộc) và quy trình đối soát/rollback. |
| P0-05 PII Kill-switch Paradox | P0.1 (Unconsented_PII_Risk + Pending_Consent_Aging) + A8 Incident SLA | Không lưu PII khi chưa consent; quá 48h cảnh báo/ép xin consent hoặc xóa. |
| P1-11 DSO Inflexible Kill | P0.3 metrics/thresholds + A8 action cards | DSO (số ngày thu tiền) là kill-switch theo tier; không bật tắt cảm tính. |
| P1-12 Unauthorized Actor | P0.2 quarantine rules + role registry | Actor_role phải nằm whitelist; sai là quarantine/reject. |
| P1-13 Missing Handover Audit | A8 Runbook + Evidence taxonomy | Thiếu bàn giao evidence/audit là không payout. |
| P2-15 No Stress Test Mode | V5 Scenario Engine module + A8 Runbook drill | Bắt buộc có stress mode (kịch bản xấu) trước go-live. |

## 4. Bổ sung trục tuổi nhà (P0-DATA-AGE) để phân nhóm hành vi
Mục tiêu: dùng tuổi nhà để phân loại nhu cầu/sản phẩm/kiểm tra hiện trường. Tuổi nhà phải là derived field (trường suy diễn) theo “as_of_date” để tránh lệch theo năm.

| Field/Metric | Đơn vị | Nguồn (evidence) | Ghi chú |
|---|---|---|---|
| built_year | năm | Giấy phép/xác nhận chủ nhà/ước lượng | Trường gốc. Có built_year_source + built_year_confidence_pct. |
| house_age_years | năm | Derived từ built_year | Trường suy diễn theo as_of_date. |
| house_age_bucket | enum | Derived | Gợi ý bucket: AGE_00_02, AGE_03_05, AGE_06_10, AGE_11_20, AGE_20P. |
| EVT_HOUSE_BUILT_YEAR_SET/UPDATED | EVT_* | evidence_pack_uri | Event append-only để cập nhật built_year. |

## 5. Chuẩn hoá metric_code: canonical + alias
Nguyên tắc: canonical metric_code phải theo hậu tố đơn vị/tỉ lệ (_hours/_days/_vnd/_rate/_pct). Tên cũ được giữ ở alias map để tương thích ngược (backward compatibility = tương thích lịch sử).

| A2 metric | Canonical metric_code | Ghi chú |
|---|---|---|
| financing_penetration | financing_penetration_rate | Nếu đã dùng tên cũ thì giữ alias. |
| bank_approval_time | bank_approval_time_hours | Chuẩn hoá đơn vị thời gian. |
| consent_rate | consent_rate | Đã chuẩn. |
| evidence_pass_rate | evidence_pass_rate | Canonical; risk_evidence_pass_rate chỉ là alias nếu tồn tại. |

## 6. Go-live checklist phải chèn vào A2 (tham chiếu A8 Runbook)
Ba mảnh bắt buộc để go-live không cháy:
1. Unit Test Spec (kiểm thử đơn vị): min_coverage, boundary cases, owner, review_required.
2. Rollback Procedures (quay lui): registry rollback, code rollback, data rollback, timebox + owner.
3. Incident Response SLA (cam kết phản ứng sự cố): Tier 1/2/3 có response_time, action_time, backup_owner, escalation.

## 7. Hướng dẫn merge (append-only) vào bộ V5
1) Không sửa A2 gốc. Thêm file overlay này như “A2_overlay_v5_0_2”.  
2) Trong V5 Front-matter: Patch Ledger thêm entry “P2-A2-ALIGN” trỏ tới overlay.  
3) Trong registry: cập nhật alias.yaml cho các metric/event nêu ở mục 5.  
4) Trong dashboard: ưu tiên canonical metric_code; hiển thị alias ở tooltip.
