import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from audit_store import append_jsonl, read_jsonl
from registry_loader import load_registries

# English → Việt:
# - scenario: kịch bản (tập giả định)
# - simulation: giả lập (chạy thử)

st.set_page_config(page_title="Scenario Panel", layout="wide")
st.title("Scenario Panel")

regs = load_registries()
repo_root = Path(regs["repo_root"]).resolve()

script = repo_root / "code" / "scripts" / "demo_scenario.py"
if not script.exists():
    st.error("Thiếu code/scripts/demo_scenario.py (merge addon)")
    st.stop()

env = os.environ.copy()
env["PYTHONPATH"] = str(repo_root / "code") + (os.pathsep + env.get("PYTHONPATH", ""))

st.caption("Chạy scenarios_demo.json (hoặc upload) để ra output so sánh. Output mặc định append-only vào data/scenario/.")

demo_path = repo_root / "demo_inputs" / "scenario" / "scenarios_demo.json"

choice = st.radio("Input", ["Use demo file", "Upload JSON"], horizontal=True)

input_path = None
if choice == "Use demo file":
    if demo_path.exists():
        input_path = demo_path
        st.success(f"Using demo: {demo_path}")
        st.json(json.loads(demo_path.read_text(encoding="utf-8")))
    else:
        st.error(f"Không thấy demo file: {demo_path}")
else:
    up = st.file_uploader("Upload scenarios json", type=["json"])
    if up is not None:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        up_dir = repo_root / "data" / "uploads" / "scenario"
        up_dir.mkdir(parents=True, exist_ok=True)
        saved = up_dir / f"{ts}__{up.name.replace(' ', '_')}"
        saved.write_bytes(up.getbuffer())
        st.success(f"Đã lưu upload (append-only): {saved}")
        input_path = saved
        st.json(json.loads(saved.read_text(encoding="utf-8")))

run_log = repo_root / "data" / "audit" / "scenario_run_log.jsonl"

if input_path is not None:
    if st.button("RUN SCENARIO", type="primary"):
        cmd = [sys.executable, str(script), "--repo_root", str(repo_root), "--input_json", str(input_path)]
        started = time.time()
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        took = time.time() - started

        append_jsonl(
            run_log,
            {
                "ts_epoch": int(time.time()),
                "input_path": str(input_path),
                "returncode": res.returncode,
                "seconds": round(took, 3),
            },
        )

        if res.returncode == 0:
            st.success("Scenario run OK")
        else:
            st.error("Scenario run FAIL")
        st.code((res.stdout or "") + "\n" + (res.stderr or ""))

st.divider()
st.subheader("Recent scenario runs (append-only log)")
rows = read_jsonl(run_log)
if rows:
    st.dataframe(rows[-200:], use_container_width=True)
else:
    st.info("Chưa có run.")
