import time
from pathlib import Path

import pandas as pd
import streamlit as st

from audit_store import append_jsonl, read_jsonl
from registry_loader import load_registries

st.set_page_config(page_title="Kill Switch Panel", layout="wide")
st.title("Kill Switch Panel")

regs = load_registries()
repo_root = Path(regs["repo_root"])
thresholds = regs["thresholds"] or {}
metrics: pd.DataFrame = regs["metrics"]
log_path = repo_root / "audit" / "kill_switch_log.jsonl"

# pick kill-switch metrics from metrics.csv (kill_switch == True)
if "kill_switch" in metrics.columns:
    ks_df = metrics[metrics["kill_switch"].astype(str).str.lower() == "true"]["metric_code"].astype(str).tolist()
else:
    ks_df = []

st.caption(f"Kill-switch metrics (from metrics.csv): {len(ks_df)}")
metric_code = st.selectbox("metric_code", ks_df if ks_df else metrics["metric_code"].astype(str).tolist())
value = st.number_input("value (giả lập)", value=0.0)

action_tier = st.selectbox("action_tier", [1, 2, 3], index=2)
notes = st.text_area("notes")

col1, col2 = st.columns(2)
with col1:
    if st.button("TRIGGER (log only)", type="primary"):
        rec = {
            "ts_epoch": int(time.time()),
            "metric_code": metric_code,
            "value": value,
            "action_tier": action_tier,
            "notes": notes,
            "mode": "SIMULATION",
        }
        append_jsonl(log_path, rec)
        st.success("Đã ghi kill-switch log (simulation).")

with col2:
    st.write("Threshold preview")
    rules = [r for r in (thresholds.get("thresholds", []) or []) if r.get("metric_code") == metric_code]
    st.json(rules[0] if rules else {})

st.divider()

st.subheader("Recent kill-switch log")
records = read_jsonl(log_path)
if records:
    df = pd.DataFrame(records)
    st.dataframe(df.sort_values(by=df.columns[0], ascending=False), use_container_width=True)
else:
    st.info("Chưa có log.")
