import streamlit as st
import pandas as pd

# Set page configuration to wide layout
st.set_page_config(
    page_title="Enterprise Health & Wellness Analytics Platform",
    layout="wide"
)

# -----------------------------------------------------------------------------
# SIDEBAR: Data Management & Cohort Filtering
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("📊 Data Management Module")
    
    # File Uploader
    uploaded_file = st.file_uploader(
        "Drop 'early_wakeup_health_dataset_cleaned.csv' here", 
        type=["csv"]
    )
    
    st.write("---")
    st.title("🎛️ Cohort Filtering Engine")
    
    # Gender Focus Filter
    gender_options = ["Female", "Male", "Non-binary"]
    selected_gender = st.multiselect(
        "Gender Focus:",
        options=gender_options,
        default=gender_options
    )
    
    # Circadian Profile Filter
    circadian_options = ["No", "Yes"]
    selected_circadian = st.multiselect(
        "Circadian Profile (Early Waker):",
        options=circadian_options,
        default=circadian_options
    )

# -----------------------------------------------------------------------------
# MAIN CONTENT AREA
# -----------------------------------------------------------------------------
st.title("🏥 Enterprise Health & Wellness Analytics Platform")
st.subheader("High-Fidelity Data Engine: Biometrics, Stressors, and Occupational Output")
st.write("---")

st.header("📊 Cross-Sectional Cohort Performance Indicators")

# Mock/Placeholder Data for KPIs (These would dynamically update based on filters)
observed_cohort = "10,000 Personnel"
avg_productivity = "7.07 / 10"
avg_stress_index = "4.52 / 10"
sleep_baseline = "7.2 Hrs"

# Create columns for the KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("### 👥 Observed Cohort")
    st.markdown(f"<h2 style='color: #3b82f6;'>{observed_cohort}</h2>", unsafe_allow_html=True)

with kpi2:
    st.markdown("### 📈 Avg Productivity")
    st.markdown(f"<h2 style='color: #3b82f6;'>{avg_productivity}</h2>", unsafe_allow_html=True)

with kpi3:
    st.markdown("### ⚡ Avg Stress Index")
    st.markdown(f"<h2 style='color: #3b82f6;'>{avg_stress_index}</h2>", unsafe_allow_html=True)

with kpi4:
    st.markdown("### 💤 Sleep Baseline")
    st.markdown(f"<h2 style='color: #3b82f6;'>{sleep_baseline}</h2>", unsafe_allow_html=True)

st.write("---")

# -----------------------------------------------------------------------------
# ANALYTICAL TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🧬 Biometric Profiles & Biomarkers", 
    "🌪️ Environmental Stressors & Mental Matrix", 
    "💼 Occupational Output Drivers"
])

with tab1:
    st.write("### Biometric Data View")
    st.info("Visualizations regarding resting heart rate, cortisol cycles, and deep sleep metrics go here.")

with tab2:
    st.write("### Environmental & Mental Metrics")
    st.info("Visualizations mapping workspace lighting, sound disruptions, and self-reported burnout scales go here.")

with tab3:
    st.write("### Occupational Output Breakdown")
    st.info("Visualizations tying sleep/stress metrics directly to project completion velocity and code/output quality metrics go here.")
