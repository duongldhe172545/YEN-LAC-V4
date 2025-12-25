# Unit Test Spec (P1-UNITTEST-SPEC)

SSOT: `governance/unit_test_spec.yaml`

## Nguyên tắc
- Mỗi `metric_code` có **tối thiểu 3 test case**: null/zero/extreme.
- Coverage tối thiểu: **90%**.
- Owner viết: Data Engineer + QA Lead review.

## Checklist cho 1 metric
1. Input null → output ổn định (thường =0 hoặc NaN theo định nghĩa).
2. Input 0 → không crash (no division by zero).
3. Extreme values → không overflow / clamp theo spec nếu có.

## Ví dụ
Xem `governance/unit_test_spec.yaml`.
