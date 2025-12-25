import pandas as pd
import streamlit as st

from registry_loader import load_registries

st.set_page_config(page_title="Registry Viewer", layout="wide")
st.title("Registry Viewer")

regs = load_registries()

choice = st.selectbox("Chọn registry", ["metrics.csv", "events.yaml", "thresholds.yaml", "metric_alias.yaml", "gate_matrix.yaml", "causal_edges.yaml", "registry_lints.yaml", "runbook_actions.yaml"])

if choice == "metrics.csv":
    df: pd.DataFrame = regs["metrics"]
    st.write(f"Rows: {len(df):,}")
    q = st.text_input("Search metric_code")
    if q:
        df = df[df["metric_code"].astype(str).str.contains(q, case=False, na=False)]
    st.dataframe(df, use_container_width=True)

elif choice == "events.yaml":
    ev = regs["events"]
    st.json(ev.get("spec", {}))
    st.subheader("Events")
    st.json(ev.get("events", ev))

elif choice == "thresholds.yaml":
    th = regs["thresholds"]
    st.json(th.get("meta", {}))
    st.subheader("Threshold rules")
    st.json(th.get("thresholds", th))

else:
    key = choice.replace(".yaml", "")
    # mapping keys
    mapping = {
        "metric_alias": "metric_alias",
        "gate_matrix": "gate_matrix",
        "causal_edges": "causal_edges",
        "registry_lints": "registry_lints",
        "runbook_actions": "runbook_actions",
    }
    st.json(regs[mapping[key]])
