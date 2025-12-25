"""
Model Lab: Revenue / Profit / Resource Simulator
Author: OK Computer AI Agent
Version: 5.0.2

Đây là mô hình giả định (what-if simulation) cho D2Com Pilot Yên Lạc.
All parameters are hypothetical and for demonstration purposes only.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Page config
st.set_page_config(
    page_title="Model Lab - Revenue/Profit Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🧪 Model Lab: Revenue / Profit / Resource Simulator")
st.caption("Đây là mô hình giả định (hypothetical what-if simulation) | This is a hypothetical model for demonstration only")

# =============================================================================
# GLOSSARY TOOLTIPS
# =============================================================================

tooltips = {
    "households_target": "Số hộ mục tiêu | Target households to reach",
    "lead_rate": "Tỷ lệ tạo lead | Lead generation rate from target households",
    "claim_rate": "Tỷ lệ CLAIMED | Percentage of leads that submit claims",
    "close_rate": "Tỷ lệ chốt FINANCIAL/GOLDEN | Conversion rate to completed sales",
    "avg_order_value_L1": "Giá trị đơn trung bình lớp L1 | Average order value for Level 1 service",
    "attach_rate_L2": "Tỷ lệ mua thêm lớp L2 | Attachment rate for Level 2 upsell",
    "avg_order_value_L2": "Giá trị đơn trung bình lớp L2 | Average order value for Level 2 service",
    "direct_cost_per_job": "Chi phí trực tiếp/job | Direct cost per completed job",
    "fixed_cost_month": "Chi phí cố định/tháng | Monthly fixed operating costs",
    "payout_rate": "Tỷ lệ chi trả incentive | Incentive payout rate to technicians",
    "refund_rate": "Tỷ lệ hoàn/huỷ | Refund/cancellation rate",
    "jobs_per_adgpro_per_week": "Năng suất thợ | Jobs completed per ADG Pro per week",
    "adgpro_active_count": "Số thợ hoạt động | Number of active installation technicians",
    "ust_productivity_touch_per_day": "Touch/lead/ngày | UST touches per lead per day",
    "field_runner_count": "Số nhân viên hiện trường | Number of field support staff",
    "dso_days": "Days Sales Outstanding | Average days to collect payment",
    "bad_debt_rate": "Tỷ lệ nợ xấu | Percentage of uncollectible receivables",
    "fraud_rate": "Tỷ lệ gian lận | Percentage of fraudulent transactions",
}

def render_tooltip(key: str):
    """Render tooltip for a parameter."""
    if key in tooltips:
        st.info(tooltips[key])

# =============================================================================
# INPUT FORM SECTIONS
# =============================================================================

st.header("📊 Input Parameters (What-If Scenario)")
st.info("All parameters are hypothetical for simulation purposes. Adjust values to see impact on revenue, profit, and capacity.")

# Create tabs for different parameter groups
tabs = st.tabs([
    "1. Market & Conversion",
    "2. Pricing & Revenue", 
    "3. Costs",
    "4. Ops & Capacity",
    "5. Cash & Risk"
])

# Default values for demo
defaults = {
    "households_target": 10000,
    "lead_rate": 0.15,
    "claim_rate": 0.70,
    "close_rate": 0.60,
    "avg_order_value_L1": 2000000,  # VND
    "attach_rate_L2": 0.30,
    "avg_order_value_L2": 1500000,  # VND
    "direct_cost_per_job": 800000,  # VND
    "fixed_cost_month": 50000000,  # VND
    "payout_rate": 0.15,
    "refund_rate": 0.05,
    "jobs_per_adgpro_per_week": 8,
    "adgpro_active_count": 20,
    "ust_productivity_touch_per_day": 3,
    "field_runner_count": 10,
    "dso_days": 30,
    "bad_debt_rate": 0.03,
    "fraud_rate": 0.01,
}

with tabs[0]:
    st.subheader("Market & Conversion Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        households_target = st.number_input(
            "households_target (số hộ mục tiêu)",
            min_value=100, max_value=100000, value=defaults["households_target"], step=100
        )
        render_tooltip("households_target")
        
        lead_rate = st.slider(
            "lead_rate (tỷ lệ tạo lead)",
            min_value=0.01, max_value=0.50, value=defaults["lead_rate"], step=0.01, format="%.2f"
        )
        render_tooltip("lead_rate")
        
        claim_rate = st.slider(
            "claim_rate (tỷ lệ CLAIMED)",
            min_value=0.10, max_value=1.00, value=defaults["claim_rate"], step=0.05, format="%.2f"
        )
        render_tooltip("claim_rate")
    
    with col2:
        close_rate = st.slider(
            "close_rate (tỷ lệ chốt FINANCIAL/GOLDEN)",
            min_value=0.10, max_value=1.00, value=defaults["close_rate"], step=0.05, format="%.2f"
        )
        render_tooltip("close_rate")
        
        # Calculate derived metrics
        leads = households_target * lead_rate
        claims = leads * claim_rate
        closed_deals = claims * close_rate
        
        st.markdown("### Derived Metrics:")
        st.metric("Total Leads", f"{leads:,.0f}")
        st.metric("Total Claims", f"{claims:,.0f}")
        st.metric("Closed Deals", f"{closed_deals:,.0f}")

with tabs[1]:
    st.subheader("Pricing & Revenue Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        avg_order_value_L1 = st.number_input(
            "avg_order_value_L1 (giá trị đơn trung bình L1) - VND",
            min_value=500000, max_value=10000000, value=defaults["avg_order_value_L1"], step=100000
        )
        render_tooltip("avg_order_value_L1")
        
        attach_rate_L2 = st.slider(
            "attach_rate_L2 (tỷ lệ mua thêm L2)",
            min_value=0.00, max_value=0.80, value=defaults["attach_rate_L2"], step=0.05, format="%.2f"
        )
        render_tooltip("attach_rate_L2")
    
    with col2:
        avg_order_value_L2 = st.number_input(
            "avg_order_value_L2 (giá trị đơn trung bình L2) - VND",
            min_value=200000, max_value=5000000, value=defaults["avg_order_value_L2"], step=50000
        )
        render_tooltip("avg_order_value_L2")
        
        # Revenue preview
        l1_customers = closed_deals
        l2_customers = closed_deals * attach_rate_L2
        
        st.markdown("### Revenue Preview:")
        st.metric("L1 Customers", f"{l1_customers:,.0f}")
        st.metric("L2 Customers", f"{l2_customers:,.0f}")

with tabs[2]:
    st.subheader("Cost Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        direct_cost_per_job = st.number_input(
            "direct_cost_per_job (chi phí trực tiếp/job) - VND",
            min_value=100000, max_value=2000000, value=defaults["direct_cost_per_job"], step=50000
        )
        render_tooltip("direct_cost_per_job")
        
        fixed_cost_month = st.number_input(
            "fixed_cost_month (chi phí cố định/tháng) - VND",
            min_value=10000000, max_value=200000000, value=defaults["fixed_cost_month"], step=1000000
        )
        render_tooltip("fixed_cost_month")
    
    with col2:
        payout_rate = st.slider(
            "payout_rate (tỷ lệ chi trả incentive)",
            min_value=0.05, max_value=0.30, value=defaults["payout_rate"], step=0.01, format="%.2f"
        )
        render_tooltip("payout_rate")
        
        refund_rate = st.slider(
            "refund_rate (tỷ lệ hoàn/huỷ)",
            min_value=0.00, max_value=0.20, value=defaults["refund_rate"], step=0.01, format="%.2f"
        )
        render_tooltip("refund_rate")

with tabs[3]:
    st.subheader("Operations & Capacity Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        jobs_per_adgpro_per_week = st.number_input(
            "jobs_per_adgpro_per_week (năng suất thợ/job/tuần)",
            min_value=1, max_value=20, value=defaults["jobs_per_adgpro_per_week"], step=1
        )
        render_tooltip("jobs_per_adgpro_per_week")
        
        adgpro_active_count = st.number_input(
            "adgpro_active_count (số thợ hoạt động)",
            min_value=1, max_value=100, value=defaults["adgpro_active_count"], step=1
        )
        render_tooltip("adgpro_active_count")
    
    with col2:
        ust_productivity_touch_per_day = st.number_input(
            "ust_productivity_touch_per_day (touch/lead/ngày)",
            min_value=1, max_value=10, value=defaults["ust_productivity_touch_per_day"], step=1
        )
        render_tooltip("ust_productivity_touch_per_day")
        
        field_runner_count = st.number_input(
            "field_runner_count (số nhân viên hiện trường)",
            min_value=1, max_value=50, value=defaults["field_runner_count"], step=1
        )
        render_tooltip("field_runner_count")
        
        # Capacity calculation
        weekly_capacity = jobs_per_adgpro_per_week * adgpro_active_count
        monthly_capacity = weekly_capacity * 4
        
        st.markdown("### Capacity:")
        st.metric("Weekly Capacity", f"{weekly_capacity:,.0f} jobs")
        st.metric("Monthly Capacity", f"{monthly_capacity:,.0f} jobs")

with tabs[4]:
    st.subheader("Cash & Risk Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        dso_days = st.number_input(
            "dso_days (Days Sales Outstanding)",
            min_value=7, max_value=90, value=defaults["dso_days"], step=1
        )
        render_tooltip("dso_days")
        
        bad_debt_rate = st.slider(
            "bad_debt_rate (tỷ lệ nợ xấu)",
            min_value=0.00, max_value=0.20, value=defaults["bad_debt_rate"], step=0.01, format="%.2f"
        )
        render_tooltip("bad_debt_rate")
    
    with col2:
        fraud_rate = st.slider(
            "fraud_rate (tỷ lệ gian lận)",
            min_value=0.00, max_value=0.10, value=defaults["fraud_rate"], step=0.005, format="%.3f"
        )
        render_tooltip("fraud_rate")

# =============================================================================
# CALCULATIONS
# =============================================================================

st.markdown("---")
st.header("📈 Calculation Results")

# Collect all parameters
params = {
    "households_target": households_target,
    "lead_rate": lead_rate,
    "claim_rate": claim_rate,
    "close_rate": close_rate,
    "avg_order_value_L1": avg_order_value_L1,
    "attach_rate_L2": attach_rate_L2,
    "avg_order_value_L2": avg_order_value_L2,
    "direct_cost_per_job": direct_cost_per_job,
    "fixed_cost_month": fixed_cost_month,
    "payout_rate": payout_rate,
    "refund_rate": refund_rate,
    "jobs_per_adgpro_per_week": jobs_per_adgpro_per_week,
    "adgpro_active_count": adgpro_active_count,
    "ust_productivity_touch_per_day": ust_productivity_touch_per_day,
    "field_runner_count": field_runner_count,
    "dso_days": dso_days,
    "bad_debt_rate": bad_debt_rate,
    "fraud_rate": fraud_rate,
}

# Calculate metrics
leads = households_target * lead_rate
claims = leads * claim_rate
closed_deals = claims * close_rate
l1_customers = closed_deals
l2_customers = closed_deals * attach_rate_L2

# Revenue
revenue_l1 = l1_customers * avg_order_value_L1
revenue_l2 = l2_customers * avg_order_value_L2
revenue_total = revenue_l1 + revenue_l2
revenue_after_refund = revenue_total * (1 - refund_rate)

# Costs
total_jobs = closed_deals
variable_costs = total_jobs * direct_cost_per_job
incentive_payout = revenue_total * payout_rate
total_costs = variable_costs + incentive_payout + fixed_cost_month
bad_debt_cost = revenue_after_refund * bad_debt_rate
fraud_cost = revenue_after_refund * fraud_rate

# Profit
gross_profit = revenue_after_refund - variable_costs - incentive_payout
net_profit = gross_profit - fixed_cost_month - bad_debt_cost - fraud_cost

# Capacity
weekly_capacity = jobs_per_adgpro_per_week * adgpro_active_count
monthly_capacity = weekly_capacity * 4
capacity_utilization = (total_jobs / monthly_capacity * 100) if monthly_capacity > 0 else 0
capacity_check = "✅ Sufficient" if capacity_utilization <= 85 else "⚠️ Overloaded" if capacity_utilization <= 100 else "❌ Backlog"

# Cash flow
avg_outstanding = revenue_after_refund * (dso_days / 30)  # Assuming monthly cycle
cash_gap_estimate = avg_outstanding * 0.3  # Simplified cash gap estimate

# Headcount
ust_required = max(1, int(leads / (ust_productivity_touch_per_day * 30)))  # Assuming 30 days

# Results dictionary
results = {
    "Revenue_L1": revenue_l1,
    "Revenue_L2": revenue_l2,
    "Revenue_Total": revenue_total,
    "Gross_Profit": gross_profit,
    "Net_Profit": net_profit,
    "Required_Headcount": {
        "UST": ust_required,
        "FieldRunner": field_runner_count,
        "ADGPro": adgpro_active_count
    },
    "Capacity_check": capacity_check,
    "Cash_gap_estimate": cash_gap_estimate,
    "Capacity_utilization": capacity_utilization,
}

# Display results in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💰 Revenue")
    st.metric("Revenue L1", f"{revenue_l1:,.0f} VND")
    st.metric("Revenue L2", f"{revenue_l2:,.0f} VND")
    st.metric("Total Revenue", f"{revenue_total:,.0f} VND")
    st.metric("After Refund", f"{revenue_after_refund:,.0f} VND")

with col2:
    st.subheader("📊 Profitability")
    st.metric("Gross Profit", f"{gross_profit:,.0f} VND")
    st.metric("Net Profit", f"{net_profit:,.0f} VND")
    
    profit_margin = (net_profit / revenue_after_refund * 100) if revenue_after_refund > 0 else 0
    st.metric("Net Margin", f"{profit_margin:.1f}%")

with col3:
    st.subheader("🏢 Operations")
    st.metric("UST Required", f"{ust_required} people")
    st.metric("Capacity Utilization", f"{capacity_utilization:.1f}%")
    st.metric("Capacity Check", capacity_check)
    st.metric("Cash Gap Est.", f"{cash_gap_estimate:,.0f} VND")

# Risk flags
risk_flags = []
if capacity_utilization > 90:
    risk_flags.append("⚠️ High capacity utilization - risk of backlog")
if profit_margin < 10:
    risk_flags.append("🔴 Low profit margin - business sustainability risk")
if bad_debt_rate > 0.05:
    risk_flags.append("🟡 High bad debt rate - collection risk")
if fraud_rate > 0.02:
    risk_flags.append("🚩 High fraud rate - security concern")

if risk_flags:
    st.subheader("🚨 Risk Flags")
    for flag in risk_flags:
        st.warning(flag)
else:
    st.success("✅ No major risk flags detected")

# =============================================================================
# VISUALIZATIONS
# =============================================================================

st.markdown("---")
st.header("📊 Visualizations")

# Waterfall chart
fig_waterfall = go.Figure(go.Waterfall(
    name="Revenue Flow",
    orientation="v",
    measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
    x=["Revenue", "Refunds", "Direct Costs", "Incentives", "Fixed Costs", "Bad Debt", "Net Profit"],
    textposition="outside",
    text=[f"{revenue_total:,.0f}", f"-{revenue_total*refund_rate:,.0f}", 
          f"-{variable_costs:,.0f}", f"-{incentive_payout:,.0f}",
          f"-{fixed_cost_month:,.0f}", f"-{bad_debt_cost:,.0f}", f"{net_profit:,.0f}"],
    y=[revenue_total, -revenue_total*refund_rate, -variable_costs, -incentive_payout,
       -fixed_cost_month, -bad_debt_cost, net_profit],
    connector={"line":{"color":"rgb(63, 63, 63)"}},
))

fig_waterfall.update_layout(
    title="Waterfall: Revenue → Costs → Profit",
    showlegend=False,
    height=500
)

st.plotly_chart(fig_waterfall, use_container_width=True)

# Capacity chart
fig_capacity = go.Figure()

fig_capacity.add_trace(go.Bar(
    name="Demand",
    x=["Jobs"],
    y=[total_jobs],
    marker_color="#ef4444"
))

fig_capacity.add_trace(go.Bar(
    name="Capacity",
    x=["Jobs"],
    y=[monthly_capacity],
    marker_color="#22c55e"
))

fig_capacity.update_layout(
    title=f"Capacity Analysis: Demand vs Capacity\nUtilization: {capacity_utilization:.1f}%",
    barmode="group",
    height=400
)

st.plotly_chart(fig_capacity, use_container_width=True)

# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

st.markdown("---")
st.header("🎯 Sensitivity Analysis")

st.markdown("Thay đổi close_rate và avg_order_value_L1 ±10% để xem ảnh hưởng")

# Base values
base_close_rate = close_rate
base_aov_l1 = avg_order_value_L1

# Create sensitivity grid
close_rates = [base_close_rate * 0.9, base_close_rate, base_close_rate * 1.1]
aov_l1_values = [base_aov_l1 * 0.9, base_aov_l1, base_aov_l1 * 1.1]

sensitivity_data = []
for cr in close_rates:
    for aov in aov_l1_values:
        # Recalculate with modified values
        temp_claims = leads * claim_rate
        temp_closed = temp_claims * cr
        temp_l1 = temp_closed * aov
        temp_l2 = temp_closed * attach_rate_L2 * avg_order_value_L2
        temp_total = temp_l1 + temp_l2
        temp_after_refund = temp_total * (1 - refund_rate)
        temp_variable = temp_closed * direct_cost_per_job
        temp_incentive = temp_total * payout_rate
        temp_gross = temp_after_refund - temp_variable - temp_incentive
        temp_net = temp_gross - fixed_cost_month
        
        sensitivity_data.append({
            "Close Rate": f"{cr:.1%}",
            "AOV L1": f"{aov:,.0f}",
            "Net Profit": temp_net,
            "Revenue": temp_total
        })

sens_df = pd.DataFrame(sensitivity_data)
pivot_profit = sens_df.pivot(index="Close Rate", columns="AOV L1", values="Net Profit")

fig_sens = px.imshow(
    pivot_profit.values,
    x=pivot_profit.columns,
    y=pivot_profit.index,
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="RdYlGn",
    title="Sensitivity: Net Profit by Close Rate and AOV L1 (VND)"
)

st.plotly_chart(fig_sens, use_container_width=True)

# =============================================================================
# SAVE RESULTS (APPEND-ONLY)
# =============================================================================

st.markdown("---")

if st.button("💾 Save This Run (Append-Only)", type="primary"):
    # Create scenario record
    scenario_record = {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "parameters": params,
        "results": results,
        "calculated_metrics": {
            "leads": leads,
            "claims": claims,
            "closed_deals": closed_deals,
            "revenue_l1": revenue_l1,
            "revenue_l2": revenue_l2,
            "revenue_total": revenue_total,
            "gross_profit": gross_profit,
            "net_profit": net_profit,
            "profit_margin": profit_margin,
            "capacity_utilization": capacity_utilization,
        },
        "risk_flags": risk_flags,
        "note": "Hypothetical what-if simulation - Model Lab run"
    }
    
    # Save to append-only file
    output_path = Path("data/scenario/whatif_runs.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(scenario_record, ensure_ascii=False) + "\n")
    
    st.success(f"✅ Scenario saved to {output_path}")
    st.json(scenario_record)

# =============================================================================
# DOWNLOAD RESULTS
# =============================================================================

st.markdown("---")
st.download_button(
    label="📄 Download Results as JSON",
    data=json.dumps({
        "parameters": params,
        "results": results,
        "timestamp": datetime.utcnow().isoformat(),
        "note": "Model Lab what-if simulation"
    }, indent=2, ensure_ascii=False),
    file_name=f"model_lab_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
    mime="application/json"
)

# Footer
st.markdown("---")
st.markdown("<small>Model Lab - Hypothetical Simulation Only | Not Real Data | For Demo Purposes</small>", 
            unsafe_allow_html=True)
