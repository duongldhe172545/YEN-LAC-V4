# Excel Master (GĐ1) — cấu trúc Tab đề xuất

## Tab Hard (dữ liệu cứng)
- HOUSE_MASTER
- ACTOR_MASTER
- JOB_MASTER
- EVENTS_GOLDEN_PATH (EVT_*)
- EVIDENCE_MANIFEST
- EVIDENCE_INDEX
- EVIDENCE_QA
- GATE_DECISION
- PAYOUT_REQUEST
- CORRECTION_EVENT
- PREFLIGHT_BATCH_CHECK

## Tab Soft (dữ liệu mềm)
- INTEL_RADAR_SNAPSHOT (TAM–SAM–SOM)
- GOV_STAKEHOLDER_MAP
- GOV_ENGAGEMENT_LOG (MoM)
- GOV_DELIVERABLES_TRACKER
- MESSAGING_REGISTRY
- BROADCAST_PLAN_LOG
- AB_CLUSTER_DESIGN
- DOOR_OPENING_LOG (DOR)
- INFLUENCE_NODE_REGISTRY
- INFLUENCE_EDGES
- ECONOMIC_SNAPSHOT
- ENTERPRISE_CENSUS
- SEASONALITY_CALENDAR
- INCIDENT_RUMOR_LOG (SOP-SOS)
- CAPACITY_CAP_PLAN
- RAIN_CHECK_BACKLOG
- DATA_OUTPUT_DELIVERY_LOG

Gợi ý: GĐ1 chạy cơm thì gộp vào 1 file Excel nhiều tab. Khi nạp máy, pipeline bóc từng tab ra thành CSV và ingest theo registry.


### Ghi chú v0.2 (2025-12-25)
- Tab GOV_* thêm cột score + reason_code.
- Tab INFLUENCE_* thêm entity_type và actor_id (nếu trùng actor_master).
- Tab JOB_MASTER thêm ust_actor_id/field_runner_actor_id/adg_actor_id.
