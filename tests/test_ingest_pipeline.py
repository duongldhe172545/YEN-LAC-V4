from pathlib import Path
import json

from core.ingest_pipeline import ingest_records


def test_ingest_quarantine_and_dedup(tmp_path: Path):
    # registry cần có -> copy từ repo thật sang temp_repo
    repo_root = Path(__file__).resolve().parents[1]
    temp_repo = tmp_path / "repo"
    temp_repo.mkdir()

    import shutil
    shutil.copytree(repo_root / "registry", temp_repo / "registry")

    (temp_repo / "data").mkdir()

    bad = {"event_code": "EVT_DISC_DRONE_SCAN_CREATED", "event_ts": "2025-12-24T10:00:00+07:00", "source_batch_id": "B1"}
    ok = {"event_code": "EVT_DISC_DRONE_SCAN_CREATED", "event_ts": "2025-12-24T10:00:00+07:00", "source_batch_id": "B1", "house_id": "H001"}
    dup = {"event_code": "EVT_DISC_DRONE_SCAN_CREATED", "event_ts": "2025-12-24T10:00:00+07:00", "source_batch_id": "B1", "house_id": "H001"}

    res = ingest_records(repo_root=temp_repo, records=[bad, ok, dup], source_batch_id="TESTBATCH")
    assert res.accepted == 1
    assert res.duplicated == 1
    assert res.quarantined == 1

    event_log = temp_repo / "data/event_store/event_log.jsonl"
    assert event_log.exists()
    lines = event_log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    obj = json.loads(lines[0])
    assert obj["event_code"] == "EVT_DISC_DRONE_SCAN_CREATED"
