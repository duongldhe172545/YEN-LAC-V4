# P0-DATA-AGE — Bản vá dữ liệu Tuổi nhà (V5.0.2)

**Patch_ID:** P0-DATA-AGE  
**Build date:** 2025-12-24  
**Effective date:** 2025-12-24  
**DDAY (Pilot):** 2026-04-01  
**Scope:** Appendix A5 (Khắc Bia Data Dictionary) + A3 (Event Registry) + A6 (Plan MasterData)

## 1) Mục tiêu
Bổ sung trục **tuổi nhà** để:
- Phân loại hành vi/nhu cầu theo vòng đời vật lý (mới xây / đã sử dụng / cũ).
- Kích hoạt checklist khảo sát, rủi ro kỹ thuật, và chiến lược cross-sell theo House_ID.
- Bám nguyên tắc **append-only**: không “update thẳng master” khi chưa có event.

## 2) Canonical fields (A5 Khắc Bia)
### 2.1 Fields gốc (source-of-truth)
| Field | Tiếng Việt | Type | Null? | Ghi chú |
|---|---|---:|:---:|---|
| built_year | Năm xây dựng | int (YYYY) | Yes | 1900..DDAY.year |
| last_major_renovation_year | Năm cải tạo lớn gần nhất | int (YYYY) | Yes | >= built_year |
| built_year_source | Nguồn năm xây | enum | Yes | OWNER_DECLARED / DOCUMENT / ESTIMATED / UNKNOWN |
| built_year_confidence_pct | Độ tin cậy % | int | Yes | 0..100 |

### 2.2 Fields dẫn xuất (derived)
| Field | Tiếng Việt | Type | Rule |
|---|---|---|---|
| house_age_bucket | Nhóm tuổi nhà | enum | Derived từ (DDAY.year - built_year) |
| house_age_years | Tuổi nhà (năm) | int | **Không lưu cứng**; tính khi query theo as_of_date |

**Bucket mặc định** (có thể điều chỉnh sau nhưng phải qua Patch Ledger):  
- UNKNOWN (built_year null)  
- AGE_00_02, AGE_03_05, AGE_06_10, AGE_11_20, AGE_20P

## 3) Canonical events (A3 Event Registry)
Các thay đổi liên quan tuổi nhà phải đi qua event:

| event_code | Mô tả | required_fields | evidence_required | idempotency_key_fields |
|---|---|---|---|---|
| EVT_HOUSE_BUILT_YEAR_SET | Set năm xây | house_id, event_at, actor_role, payload.built_year | Yes | house_id, payload.built_year, event_at_date |
| EVT_HOUSE_BUILT_YEAR_UPDATED | Update năm xây (có lý do) | + payload.reason | Yes | house_id, payload.built_year, payload.reason |
| EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_SET | Set năm cải tạo | + payload.last_major_renovation_year | Yes | house_id, payload.last_major_renovation_year, event_at_date |
| EVT_HOUSE_LAST_MAJOR_RENOVATION_YEAR_UPDATED | Update năm cải tạo | + payload.reason | Yes | house_id, payload.last_major_renovation_year, payload.reason |

**State impact:** Không chuyển `house_lifecycle_status` (vì đây là thuộc tính vật lý), chỉ cập nhật master snapshot sau khi event hợp lệ.

## 4) Alias map (tương thích ngược)
| Legacy | Canonical |
|---|---|
| year_built | built_year |
| house_year_built | built_year |
| renovation_year | last_major_renovation_year |

## 5) Quarantine/Reject rules (tối thiểu)
- Reject nếu built_year < 1900 hoặc > DDAY.year  
- Reject nếu last_major_renovation_year < built_year (khi cả hai có)  
- Quarantine nếu built_year_source=OWNER_DECLARED và confidence_pct < 50 (yêu cầu bổ sung bằng chứng)

## 6) Pass/Fail (đóng patch)
PASS khi:
- A5 có đủ fields + units + enums như mục 2.
- A3 có đủ 4 event như mục 3, kèm required_fields + evidence_required + idempotency.
- Alias map có đủ 3 mapping như mục 4.

FAIL khi:
- Có field tuổi nhà ở canonical mà không có event tương ứng.
- built_year/renovation_year bị ghi trực tiếp vào master mà không có event.

## 7) Rollback
- Revert commit của registry/events + dictionary fields.
- Rebuild snapshot từ event_log (bỏ qua các event P0-DATA-AGE) nếu cần.
