# P1-UNITTEST-SPEC (V5.0.2) — 2025-12-24

## Mục tiêu
Khóa quy định Unit Test để dev không tự đoán → giảm bug KPI.

## SSOT
- `governance/unit_test_spec.yaml`
- (doc) `docs/governance/Unit_Test_Spec.md`

## Overlay vào Hiến Pháp (gợi ý vị trí)
- Section 14.3.2: Unit Test Spec

## Checklist PASS/FAIL
PASS khi:
- Repo có spec YAML
- CI chạy `pytest -q` và `validate_registry.py` PASS
- Mỗi metric mới bổ sung phải kèm test theo 3 boundary
