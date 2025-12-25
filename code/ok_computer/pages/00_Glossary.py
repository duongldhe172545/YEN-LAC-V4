"""
Glossary & Definitions Page
Author: OK Computer AI Agent
Version: 5.0.2

Anh-Việt chuẩn hoá | Standardized terminology reference | Registry-First
"""

import csv
import json
from pathlib import Path
from typing import Dict, Any

import streamlit as st

# Page config
st.set_page_config(
    page_title="Glossary & Definitions",
    layout="wide"
)

# Title
st.title("📖 Glossary & Definitions")
st.caption("Anh-Việt chuẩn hoá | Standardized Terminology Reference | Registry-First")

# Load glossary from registry (SSOT)
@st.cache_data
def load_glossary() -> Dict[str, Dict[str, Any]]:
    """Load glossary from registry/glossary.csv (registry-first principle)."""
    glossary = {}
    
    registry_path = Path("registry/glossary.csv")
    provisional_path = Path("data/glossary_provisional.csv")
    
    # Try registry first (SSOT)
    if registry_path.exists():
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    term_code = row.get('term_code', '').strip()
                    if term_code:
                        glossary[term_code] = {
                            'en': row.get('en', ''),
                            'vi': row.get('vi', ''),
                            'definition_en': row.get('definition_en', ''),
                            'definition_vi': row.get('definition_vi', ''),
                            'unit': row.get('unit', ''),
                            'example': row.get('example', ''),
                            'source': row.get('source', 'registry')
                        }
        except Exception as e:
            st.error(f"Error reading registry glossary: {e}")
    
    # Fallback to provisional if registry not available
    elif provisional_path.exists():
        try:
            with open(provisional_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    term_code = row.get('term_code', '').strip()
                    if term_code:
                        glossary[term_code] = {
                            'en': row.get('en', ''),
                            'vi': row.get('vi', ''),
                            'definition_en': row.get('definition_en', ''),
                            'definition_vi': row.get('definition_vi', ''),
                            'unit': row.get('unit', ''),
                            'example': row.get('example', ''),
                            'source': row.get('source', 'PROVISIONAL')
                        }
            st.warning("Using provisional glossary - registry/glossary.csv not found")
        except Exception as e:
            st.error(f"Error reading provisional glossary: {e}")
    
    # If neither exists, create provisional with minimum terms
    if not glossary:
        st.warning("No glossary found - creating provisional with minimum terms")
        
        # Create minimum glossary
        min_glossary = {
            "KPI": {
                "en": "Key Performance Indicator",
                "vi": "Chỉ số đo hiệu suất",
                "definition_en": "Metric used to evaluate success of an organization",
                "definition_vi": "Metric dùng để đánh giá hiệu suất tổ chức",
                "unit": "Various",
                "example": "K0 = Data Quality Score",
                "source": "PROVISIONAL"
            },
            "EVT": {
                "en": "Event",
                "vi": "Sự kiện",
                "definition_en": "A canonical event record with event_code format EVT_[A-Z0-9_]+",
                "definition_vi": "Bản ghi sự kiện chuẩn với định dạng EVT_[A-Z0-9_]+",
                "unit": "Event record",
                "example": "EVT_LEAD_CREATED",
                "source": "PROVISIONAL"
            },
            "DSO": {
                "en": "Days Sales Outstanding",
                "vi": "Số ngày thu tiền bình quân",
                "definition_en": "Average number of days to collect payment after sale",
                "definition_vi": "Số ngày trung bình thu tiền sau bán hàng",
                "unit": "Days",
                "example": "DSO = 30 means payment collected in 30 days",
                "source": "PROVISIONAL"
            },
            "PII": {
                "en": "Personally Identifiable Information",
                "vi": "Thông tin định danh cá nhân",
                "definition_en": "Any information that can identify a specific individual",
                "definition_vi": "Thông tin có thể xác định cá nhân cụ thể",
                "unit": "Data classification",
                "example": "Name phone ID card number address",
                "source": "PROVISIONAL"
            },
            "Evidence": {
                "en": "Evidence",
                "vi": "Bằng chứng",
                "definition_en": "Proof required to validate service delivery and trigger payment",
                "definition_vi": "Bằng chứng cần thiết để xác nhận dịch vụ và kích hoạt thanh toán",
                "unit": "Document/record",
                "example": "Photo of installed equipment GPS coordinates",
                "source": "PROVISIONAL"
            },
            "UST": {
                "en": "UST (Urban Sales Team)",
                "vi": "Đại diện thương mại địa phương",
                "definition_en": "Sales team handling urban area leads",
                "definition_vi": "Đội ngũ bán hàng xử lý lead khu vực đô thị",
                "unit": "Team/Role",
                "example": "UST productivity = 3 touches/lead/day",
                "source": "PROVISIONAL"
            },
            "L1": {
                "en": "Level 1 Service",
                "vi": "Biên sản phẩm lõi",
                "definition_en": "Primary service tier representing basic package",
                "definition_vi": "Cấp dịch vụ chính đại diện gói cơ bản",
                "unit": "Service tier",
                "example": "L1 = basic internet installation 2000000 VND",
                "source": "PROVISIONAL"
            },
            "L2": {
                "en": "Level 2 Service",
                "vi": "Cross-sell theo vòng đờ House_ID",
                "definition_en": "Secondary service tier representing premium package",
                "definition_vi": "Cấp dịch vụ thứ hai đại diện gói cao cấp",
                "unit": "Service tier",
                "example": "L2 = premium package upsell 1500000 VND",
                "source": "PROVISIONAL"
            }
        }
        
        # Write provisional glossary
        provisional_path.parent.mkdir(parents=True, exist_ok=True)
        with open(provisional_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['term_code', 'en', 'vi', 'definition_en', 'definition_vi', 'unit', 'example', 'source'])
            writer.writeheader()
            for term_code, data in min_glossary.items():
                writer.writerow({
                    'term_code': term_code,
                    'en': data['en'],
                    'vi': data['vi'],
                    'definition_en': data['definition_en'],
                    'definition_vi': data['definition_vi'],
                    'unit': data['unit'],
                    'example': data['example'],
                    'source': 'PROVISIONAL'
                })
        
        glossary = min_glossary
    
    return glossary

# Load glossary
glossary = load_glossary()

# Search functionality
st.markdown("### 🔍 Search Glossary")
search_term = st.text_input("Enter search term:", placeholder="e.g., KPI, Evidence, DSO...")

# Filter glossary based on search
if search_term:
    filtered_glossary = {
        k: v for k, v in glossary.items() 
        if (search_term.lower() in k.lower() or 
            search_term.lower() in v['en'].lower() or 
            search_term.lower() in v['vi'].lower() or
            search_term.lower() in v['definition_en'].lower())
    }
else:
    filtered_glossary = glossary

# Display glossary terms
st.markdown(f"### 📚 Showing {len(filtered_glossary)} terms")

for term_code, term_info in sorted(filtered_glossary.items()):
    with st.expander(f"**{term_code}** - {term_info['en']}"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"**English:** {term_info['en']}")
            st.markdown(f"**Tiếng Việt:** {term_info['vi']}")
            st.markdown(f"**Unit:** `{term_info['unit']}`")
            st.markdown(f"**Source:** `{term_info['source']}`")
        
        with col2:
            st.markdown(f"**Definition:**\n{term_info['definition_en']}")
            st.markdown(f"**Ví dụ:**\n`{term_info['example']}`")

# Summary statistics
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Terms", len(glossary))

with col2:
    provisional_count = len([k for k in glossary.keys() if glossary[k].get('source') == 'PROVISIONAL'])
    st.metric("Provisional Terms", provisional_count)

with col3:
    registry_count = len([k for k in glossary.keys() if glossary[k].get('source') != 'PROVISIONAL'])
    st.metric("Registry Terms", registry_count)

# Footer
st.markdown("---")
st.markdown("<small>Glossary & Definitions | OK Computer D2Com Pilot Yên Lạc V5.0.2 | Registry-First Standard</small>", 
            unsafe_allow_html=True)
