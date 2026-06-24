import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. PAGE SETUP
st.set_page_config(
    page_title="Enterprise Health & Wellness Analytics Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. SIDEBAR: DATA MANAGEMENT & COHORT FILTERING ENGINE
with st.sidebar:
    st.markdown("## 💾 Data Management Module")
    
    # Drag and drop file uploader mock
    uploaded_file = st.file_uploader(
        "Drop 'early_wakeup_health_dataset_cleaned.csv' here", 
        type=["csv"],
        help="Upload your enterprise wellness dataset here."
    )
    if uploaded_file is not None:
        st.success("Dataset loaded successfully!")
    else:
        st.caption("Using pre-loaded internal high-fidelity mock engine data.")
        
    st.write("---")
    st.markdown("## 🎛️ Cohort Filtering Engine")
    
    # Gender Filters
    gender_options = ["Female", "Male", "Non-binary"]
    selected_gender = st.multiselect(
        "Gender Focus:",
        options=gender_options,
        default=gender_options
    )
    
    # Circadian Profile Filters
    circadian_options = ["Yes", "No"]
    selected_circadian = st.multiselect(
        "Circadian Profile (Early Waker):",
        options=circadian_options,
        default=circadian_options
    )
    
    st.write("---")
    st.caption("⚡ Powered by High-Fidelity Analytics Engine v2.4")

# 3. MAIN DASHBOARD HEADER
st.markdown("# 🏥 Enterprise Health & Wellness Analytics Platform")
st.markdown("### High-Fidelity Data Engine: Biometrics, Stressors, and Occupational Output")
st.write("---")

# 4. CROSS-SECTIONAL COHORT PERFORMANCE INDICATORS (KPIs)
st.markdown("## 📊 Cross-Sectional Cohort Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("### 👥 Observed Cohort")
    st.markdown("<h2 style='color: #4A90E2; margin-top:-15px;'>10,000 Personnel</h2>", unsafe_allow_html=True)

with kpi2:
    st.markdown("### 📈 Avg Productivity")
    st.markdown("<h2 style='color: #4A90E2; margin-top:-15px;'>7.07 / 10</h2>", unsafe_allow_html=True)

with kpi3:
    st.markdown("### ⚡ Avg Stress Index")
    st.markdown("<h2 style='color: #4A90E2; margin-top:-15px;'>4.52 / 10</h2>", unsafe_allow_html=True)

with kpi4:
    st.markdown("### 💤 Sleep Baseline")
    st.markdown("<h2 style='color: #4A90E2; margin-top:-15px;'>7.2 Hrs</h2>", unsafe_allow_html=True)

st.write("---")

# 5. CORE ANALYTICAL MATRIX (THE THREE SECTIONS)
tab1, tab2, tab3 = st.tabs([
    "🧬 Biometric Profiles & Biomarkers", 
    "🌪️ Environmental Stressors & Mental Matrix", 
    "💼 Occupational Output Drivers"
])

# -----------------------------------------------------------------------------
# TAB 1: BIOMETRIC PROFILES & BIOMARKERS
# -----------------------------------------------------------------------------
with tab1:
    st.markdown("## 🧬 Biometric Data Deep Dive")
    
    # Data Engine Mock for Tab 1
    np.random.seed(42)
    hours_24 = list(range(24))
    cortisol_curve = 5 + 15 * np.exp(-((np.array(hours_24) - 7) / 3)**2) + np.random.normal(0, 0.4, 24)
    df_cortisol = pd.DataFrame({"Hour of Day": hours_24, "Cortisol Level (mcg/dL)": cortisol_curve})
    
    sleep_stages = ["Deep Sleep", "REM Sleep", "Light Sleep", "Awake"]
    sleep_minutes = [78, 92, 218, 44]
    df_sleep = pd.DataFrame({"Stage": sleep_stages, "Minutes": sleep_minutes})
    
    rhr_data = np.random.normal(loc=62, scale=6, size=1000)
    df_rhr = pd.DataFrame({"Resting Heart Rate (BPM)": rhr_data})
    
    # Layout Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⏳ 24-Hour Cortisol Cycle Dynamics")
        fig_cortisol = px.line(df_cortisol, x="Hour of Day", y="Cortisol Level (mcg/dL)",
                               title="Circadian Cortisol Curve", markers=True, template="plotly_dark")
        st.plotly_chart(fig_cortisol, use_container_width=True)
        
    with col2:
        st.markdown("#### 📊 Sleep Architecture Distribution")
        fig_sleep = px.pie(df_sleep, values="Minutes", names="Stage", 
                           title="Average Sleep Stage Distribution", hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_sleep, use_container_width=True)
        
    st.markdown("#### 💓 Cohort Resting Heart Rate (RHR) Spread")
    fig_rhr = px.histogram(df_rhr, x="Resting Heart Rate (BPM)", nbins=35, 
                           title="RHR Logged Frequency Matrix", color_discrete_sequence=['#4A90E2'], template="plotly_dark")
    st.plotly_chart(fig_rhr, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: ENVIRONMENTAL STRESSORS & MENTAL MATRIX
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("## 🌪️ Environmental Stressors & Burnout Correlations")
    
    # Data Engine Mock for Tab 2
    np.random.seed(24)
    n_samples = 400
    sound_db = np.random.uniform(45, 85, n_samples)
    light_lux = np.random.uniform(150, 750, n_samples)
    burnout_index = np.clip((sound_db * 0.07) - (light_lux * 0.0015) + np.random.normal(2, 0.8, n_samples), 1, 10)
    zones = np.random.choice(["Open Plan Space", "Focus Cubicles", "Meeting Hubs", "Remote Office"], n_samples)
    df_env = pd.DataFrame({"Sound Disruptions (dB)": sound_db, "Lighting (Lux)": light_lux, "Burnout Scale (1-10)": burnout_index, "Office Zone": zones})
    
    # Layout Grid
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🔊 Ambient Noise Cross-Analysis")
        fig_sound = px.scatter(df_env, x="Sound Disruptions (dB)", y="Burnout Scale (1-10)", 
                               color="Office Zone", trendline="ols", title="Noise Stressors vs Burnout Curve", template="plotly_dark")
        st.plotly_chart(fig_sound, use_container_width=True)
        
    with col4:
        st.markdown("#### 💡 Luminescence Matrix")
        fig_light = px.scatter(df_env, x="Lighting (Lux)", y="Burnout Scale (1-10)", 
                               color="Office Zone", trendline="ols", title="Illuminance Levels vs Burnout Index", template="plotly_dark")
        st.plotly_chart(fig_light, use_container_width=True)
        
    st.markdown("#### 🏢 Burnout Concentration Index by Workplace Setting")
    df_zone = df_env.groupby("Office Zone")["Burnout Scale (1-10)"].mean().reset_index()
    fig_zone = px.bar(df_zone, x="Office Zone", y="Burnout Scale (1-10)", color="Office Zone", template="plotly_dark")
    st.plotly_chart(fig_zone, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: OCCUPATIONAL OUTPUT DRIVERS
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("## 💼 Occupational Output Drivers & Performance Optimization")
    
    # Data Engine Mock for Tab 3
    np.random.seed(88)
    n_sprints = 250
    sleep_h = np.random.uniform(4.5, 9.0, n_sprints)
    stress_idx = np.random.uniform(1.0, 10.0, n_sprints)
    velocity = np.clip((sleep_h * 4.0) - (stress_idx * 1.5) + np.random.normal(12, 2.5, n_sprints), 5, 45)
    quality = np.clip((sleep_h * 11) - (stress_idx * 4.0) + np.random.normal(45, 6, n_sprints), 10, 100)
    df_output = pd.DataFrame({"Sleep (Hours)": sleep_h, "Stress Index": stress_idx, "Sprint Velocity": velocity, "Quality Score (%)": quality})
    
    # Layout Grid
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 🚀 Sleep Rest Patterns vs. Velocity Metrics")
        fig_vel = px.scatter(df_output, x="Sleep (Hours)", y="Sprint Velocity", color="Stress Index",
                             trendline="lowess", title="Impact of System Fatigue on Delivery Speeds", template="plotly_dark")
        st.plotly_chart(fig_vel, use_container_width=True)
        
    with col6:
        st.markdown("#### 🎯 Human Stress Factors vs. Technical Quality")
        fig_qual = px.scatter(df_output, x="Stress Index", y="Quality Score (%)", color="Sleep (Hours)",
                              trendline="ols", title="Defect Rates vs Mental Friction Matrix", template="plotly_dark")
        st.plotly_chart(fig_qual, use_container_width=True)
        
    st.markdown("#### 📊 Risk Quadrant Assessment: Velocity and QA Decay Matrix")
    df_output['Risk Profile'] = 'Optimized Performance'
    df_output.loc[(df_output['Sleep (Hours)'] < 6.5) & (df_output['Stress Index'] > 6.0), 'Risk Profile'] = 'Severe Burnout Risk'
    df_output.loc[(df_output['Sleep (Hours)'] >= 6.5) & (df_output['Stress Index'] > 6.0), 'Risk Profile'] = 'High Friction Workload'
    df_output.loc[(df_output['Sleep (Hours)'] < 6.5) & (df_output['Stress Index'] <= 6.0), 'Risk Profile'] = 'Sleep Depleted Output'
    
    df_risk = df_output.groupby("Risk Profile")[["Sprint Velocity", "Quality Score (%)"]].mean().reset_index()
    st.dataframe(df_risk.style.background_gradient(cmap="YlOrRd", subset=["Sprint Velocity", "Quality Score (%)"]), use_container_width=True)
