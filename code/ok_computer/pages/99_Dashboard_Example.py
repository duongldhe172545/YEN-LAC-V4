"""
🎯 Dashboard Example - Best Practices Implementation
Author: OK Computer AI Agent
Version: 5.0.2

Ví dụ về cách thiết kế dashboard khoa học và đẹp mắt
"""

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Dashboard Example - Best Practices",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3498db;
    }
    
    /* Cards */
    .info-card {
        background: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    /* Status badges */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
    }
    
    .status-warning {
        background: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
    }
    
    .status-danger {
        background: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🎯 D2Com Pilot Yên Lạc - Dashboard Best Practices")
st.caption("Ví dụ về cách thiết kế dashboard khoa học và chuyên nghiệp")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Time range selector
    time_range = st.selectbox(
        "📅 Time Range",
        options=["Last 24 hours", "Last 7 days", "Last 30 days", "All time"],
        index=0
    )
    
    # Metric selection
    st.subheader("📊 Metrics to Display")
    show_events = st.checkbox("Events", value=True)
    show_houses = st.checkbox("Houses", value=True)
    show_revenue = st.checkbox("Revenue", value=True)
    show_compliance = st.checkbox("Compliance", value=True)
    
    # Auto refresh
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
    if auto_refresh:
        st_autorefresh(interval=5000, key="auto_refresh")

# Generate sample data based on time range
@st.cache_data(ttl=60)
def generate_sample_data(time_range):
    base_events = 1500
    base_houses = 8500
    base_revenue = 1250000
    
    if time_range == "Last 24 hours":
        multiplier = 0.1
    elif time_range == "Last 7 days":
        multiplier = 0.7
    elif time_range == "Last 30 days":
        multiplier = 1.0
    else:  # All time
        multiplier = 2.5
    
    return {
        "events": int(base_events * multiplier),
        "houses": int(base_houses * multiplier),
        "revenue": base_revenue * multiplier,
        "quarantine": int(50 * multiplier),
        "accuracy": 99.8,
        "processing_time": 2.3
    }

data = generate_sample_data(time_range)

# Main KPI Cards
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if show_events:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{data["events"]:,}</div>
            <div class="metric-label">📊 Events Processed</div>
            <div class="metric-delta">↑ +12% vs yesterday</div>
        </div>
        ''', unsafe_allow_html=True)

with col2:
    if show_houses:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-value">{data["houses"]:,}</div>
            <div class="metric-label">🏠 Houses Tracked</div>
            <div class="metric-delta">↑ +8% this week</div>
        </div>
        ''', unsafe_allow_html=True)

with col3:
    if show_revenue:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-value">${data["revenue"]:,.0f}</div>
            <div class="metric-label">💰 Revenue Generated</div>
            <div class="metric-delta">↑ +15% vs target</div>
        </div>
        ''', unsafe_allow_html=True)

with col4:
    if show_compliance:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-value">{data["accuracy"]}%</div>
            <div class="metric-label">✅ Data Accuracy</div>
            <div class="metric-delta">↑ +0.2% vs SLA</div>
        </div>
        ''', unsafe_allow_html=True)

# Second row - Charts
st.markdown('<div class="section-header">📊 Data Visualization</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📈 Event Processing Over Time")
    
    # Generate time series data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    events_daily = [45 + i*2 + (i%7)*5 for i in range(len(dates))]
    
    df_time = pd.DataFrame({
        'Date': dates,
        'Events': events_daily
    })
    
    fig_time = px.line(
        df_time, 
        x='Date', 
        y='Events',
        title='Daily Event Processing',
        color_discrete_sequence=['#007bff']
    )
    fig_time.update_layout(
        height=300,
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col_right:
    st.subheader("🎯 Event Status Distribution")
    
    status_data = {
        'Status': ['Accepted', 'Quarantined', 'Processing'],
        'Count': [data['events'] - data['quarantine'], data['quarantine'], 23],
        'Color': ['#28a745', '#dc3545', '#ffc107']
    }
    
    fig_pie = px.pie(
        status_data,
        values='Count',
        names='Status',
        color='Status',
        color_discrete_map={
            'Accepted': '#28a745',
            'Quarantined': '#dc3545',
            'Processing': '#ffc107'
        }
    )
    fig_pie.update_layout(
        height=300,
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Third row - Tables and details
st.markdown('<div class="section-header">📋 Recent Activity</div>', unsafe_allow_html=True)

tabs = st.tabs(["✅ Accepted Events", "🚫 Quarantined Events", "📊 Analytics"])

with tabs[0]:
    # Sample accepted events table
    accepted_events = [
        {
            "Event Code": "EVT_DISC_DRONE_SCAN_CREATED",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "House ID": "YNL_001",
            "Status": "<span class='status-success'>ACCEPTED</span>",
            "PII": "No"
        },
        {
            "Event Code": "EVT_VER_HOUSE_QUALIFIED",
            "Timestamp": (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "House ID": "YNL_002",
            "Status": "<span class='status-success'>ACCEPTED</span>",
            "PII": "Yes (Consented)"
        },
        {
            "Event Code": "EVT_VER_CONSENT_OTP_VERIFIED",
            "Timestamp": (datetime.now() - timedelta(minutes=12)).strftime("%Y-%m-%d %H:%M:%S"),
            "House ID": "YNL_003",
            "Status": "<span class='status-success'>ACCEPTED</span>",
            "PII": "Yes (Consented)"
        }
    ]
    
    df_accepted = pd.DataFrame(accepted_events)
    st.markdown(df_accepted.to_html(escape=False, index=False), unsafe_allow_html=True)

with tabs[1]:
    # Sample quarantined events
    quarantined_events = [
        {
            "Event Code": "EVT_INVALID_DATA",
            "Timestamp": (datetime.now() - timedelta(minutes=8)).strftime("%Y-%m-%d %H:%M:%S"),
            "House ID": "BAD_001",
            "Reason": "Invalid phone format",
            "Status": "<span class='status-danger'>QUARANTINED</span>",
            "Correction": "✅ Possible"
        },
        {
            "Event Code": "EVT_MISSING_CONSENT",
            "Timestamp": (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
            "House ID": "BAD_002",
            "Reason": "Missing consent flag",
            "Status": "<span class='status-danger'>QUARANTINED</span>",
            "Correction": "❌ Not possible"
        }
    ]
    
    df_quarantined = pd.DataFrame(quarantined_events)
    st.markdown(df_quarantined.to_html(escape=False, index=False), unsafe_allow_html=True)

with tabs[2]:
    col_analytics1, col_analytics2 = st.columns(2)
    
    with col_analytics1:
        st.subheader("⚡ Performance Metrics")
        st.metric("Processing Speed", f"{data['processing_time']}s", "-0.2s vs target")
        st.metric("Throughput", "1,500 events/h", "+50% capacity")
        st.metric("Error Rate", "0.2%", "-0.1% vs SLA")
    
    with col_analytics2:
        st.subheader("🔒 Compliance Status")
        
        compliance_items = [
            ("PII Protection", "100%", "✅"),
            ("Data Lineage", "100%", "✅"),
            ("Audit Trail", "100%", "✅"),
            ("Consent Tracking", "100%", "✅")
        ]
        
        for item, value, status in compliance_items:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(item)
            col2.write(value)
            col3.write(status)

# Info section
st.markdown('<div class="section-header">ℹ️ System Information</div>', unsafe_allow_html=True)

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown('''
    <div class="info-card">
        <h4>🚀 Performance</h4>
        <ul>
            <li>Processing: Real-time</li>
            <li>Latency: < 3 seconds</li>
            <li>Throughput: 1,500 events/h</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

with info_col2:
    st.markdown('''
    <div class="info-card">
        <h4>🔒 Security</h4>
        <ul>
            <li>PII: Encrypted at rest</li>
            <li>Access: Role-based</li>
            <li>Audit: Full trail</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

with info_col3:
    st.markdown('''
    <div class="info-card">
        <h4>📊 Scalability</h4>
        <ul>
            <li>Horizontal scaling</li>
            <li>Load balancing</li>
            <li>Auto-scaling enabled</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <small>
        🎯 Dashboard Best Practices Example | OK Computer D2Com Pilot Yên Lạc V5.0.2<br>
        Built with Streamlit • Data updated in real-time • Compliance verified
    </small>
</div>
""", unsafe_allow_html=True)

# Add auto-refresh functionality
if auto_refresh:
    # This will trigger a rerun every 5 seconds
    import time
    time.sleep(1)
    st.rerun()
