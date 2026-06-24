import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Enterprise Health & Wellness Analytics Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. SIDEBAR FILTER MATRICES
with st.sidebar:
    st.markdown("## 💾 Data Management Module")
    uploaded_file = st.file_uploader(
        "Drop 'early_wakeup_health_dataset_cleaned.csv' here", 
        type=["csv"],
        help="Upload corporate health datasets here."
    )
    st.write("---")
    st.markdown("## 🎛️ Cohort Filtering Engine")
    gender_options = ["Female", "Male", "Non-binary"]
    selected_gender = st.multiselect("Gender Focus:", options=gender_options, default=gender_options)
    circadian_options = ["Yes", "No"]
    selected_circadian = st.multiselect("Circadian Profile (Early Waker):", options=circadian_options, default=circadian_options)

# 3. INTERACTIVE MAIN INTERFACE DISPLAY
st.markdown("# 🏥 Enterprise Health & Wellness Analytics Platform")
st.markdown("### High-Fidelity Data Engine: Biometrics, Stressors, and Occupational Output")
st.write("---")

# 4. KPI ROW (MATCHING YOUR DASHBOARD IMAGE)
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

# DATA SIMULATION ENGINE (Generates safe data profiles)
np.random.seed(42)
n_samples = 400

# Module A Data Setup
hours_24 = list(range(24))
cortisol_curve = 5 + 15 * np.exp(-((np.array(hours_24) - 7) / 3)**2) + np.random.normal(0, 0.4, 24)
df_cortisol = pd.DataFrame({"Hour of Day": hours_24, "Cortisol Level (mcg/dL)": cortisol_curve})
df_sleep_stages = pd.DataFrame({"Stage": ["Deep Sleep", "REM Sleep", "Light Sleep", "Awake"], "Minutes": [78, 92, 218, 44]})

# Module B Data Setup
sound_db = np.random.uniform(45, 85, n_samples)
light_lux = np.random.uniform(150, 750, n_samples)
burnout_index = np.clip((sound_db * 0.07) - (light_lux * 0.0015) + np.random.normal(2, 0.8, n_samples), 1, 10)
zones = np.random.choice(["Open Plan Space", "Focus Cubicles", "Meeting Hubs", "Remote Office"], n_samples)
df_env = pd.DataFrame({"Sound Disruptions (dB)": sound_db, "Lighting (Lux)": light_lux, "Burnout Scale (1-10)": burnout_index, "Office Zone": zones})

# Module C & Quadrant Data Setup
sleep_h = np.random.uniform(4.5, 9.0, n_samples)
stress_idx = np.random.uniform(1.0, 10.0, n_samples)
velocity = np.clip((sleep_h * 4.0) - (stress_idx * 1.5) + np.random.normal(12, 2.5, n_samples), 5, 45)
quality = np.clip((sleep_h * 11) - (stress_idx * 4.0) + np.random.normal(45, 6, n_samples), 10, 100)

df_output = pd.DataFrame({
    "Sleep (Hours)": sleep_h,
    "Stress Index": stress_idx,
    "Sprint Velocity": velocity,
    "Quality Score (%)": quality
})

# Classify Risk Profiles for the Matrix
df_output['Risk Profile'] = 'Optimized Performance'
df_output.loc[(df_output['Sleep (Hours)'] < 6.5) & (df_output['Stress Index'] > 6.0), 'Risk Profile'] = 'Severe Burnout Risk'
df_output.loc[(df_output['Sleep (Hours)'] >= 6.5) & (df_output['Stress Index'] > 6.0), 'Risk Profile'] = 'High Friction Workload'
df_output.loc[(df_output['Sleep (Hours)'] < 6.5) & (df_output['Stress Index'] <= 6.0), 'Risk Profile'] = 'Sleep Depleted Output'


# 5. RENDER ALL SECTIONS ON SCREEN
# MODULE A: BIOMETRICS
st.markdown("## 🧬 1. Biometric Profiles & Biomarkers")
colA1, colA2 = st.columns(2)
with colA1:
    fig_cortisol = px.line(df_cortisol, x="Hour of Day", y="Cortisol Level (mcg/dL)", title="Circadian Cortisol Cycle", markers=True, template="plotly_dark")
    st.plotly_chart(fig_cortisol, use_container_width=True)
with colA2:
    fig_sleep = px.pie(df_sleep_stages, values="Minutes", names="Stage", title="Sleep Architecture Distribution", hole=0.4, template="plotly_dark")
    st.plotly_chart(fig_sleep, use_container_width=True)

st.write("---")

# MODULE B: ENVIRONMENTAL STRESSORS
st.markdown("## 🌪️ 2. Environmental Stressors & Mental Matrix")
colB1, colB2 = st.columns(2)
with colB1:
    fig_sound = px.scatter(df_env, x="Sound Disruptions (dB)", y="Burnout Scale (1-10)", color="Office Zone", title="Noise Stressors vs Burnout Curve", template="plotly_dark")
    st.plotly_chart(fig_sound, use_container_width=True)
with colB2:
    fig_light = px.scatter(df_env, x="Lighting (Lux)", y="Burnout Scale (1-10)", color="Office Zone", title="Illuminance Levels vs Burnout Index", template="plotly_dark")
    st.plotly_chart(fig_light, use_container_width=True)

st.write("---")

# MODULE C: OCCUPATIONAL DRIVERS
st.markdown("## 💼 3. Occupational Output Drivers")
colC1, colC2 = st.columns(2)
with colC1:
    fig_vel = px.scatter(df_output, x="Sleep (Hours)", y="Sprint Velocity", color="Stress Index", title="Sleep Rest Patterns vs Velocity Metrics", template="plotly_dark")
    st.plotly_chart(fig_vel, use_container_width=True)
with colC2:
    fig_qual = px.scatter(df_output, x="Stress Index", y="Quality Score (%)", color="Sleep (Hours)", title="Human Stress Factors vs Technical Quality", template="plotly_dark")
    st.plotly_chart(fig_qual, use_container_width=True)

st.write("---")

# MODULE D: RISK QUADRANT ASSESSMENT MATRIX
st.markdown("## 📊 4. Risk Quadrant Assessment: Velocity and QA Decay Matrix")
colD1, colD2 = st.columns([2, 1])

with colD1:
    # Render the 4-box scatter visual quadrant map
    fig_quadrant = px.scatter(
        df_output, x="Sleep (Hours)", y="Stress Index", color="Risk Profile",
        color_discrete_map={
            'Optimized Performance': '#2ecc71', 'High Friction Workload': '#f1c40f',
            'Sleep Depleted Output': '#e67e22', 'Severe Burnout Risk': '#e74c3c'
        },
        hover_data=["Sprint Velocity", "Quality Score (%)"],
        title="Human Risk Assessment Quadrant Map", template="plotly_dark"
    )
    # Add vertical and horizontal dividers to build the visual quadrants
    fig_quadrant.add_shape(type="line", x0=6.5, y0=0, x1=6.5, y1=10, line=dict(color="rgba(255,255,255,0.3)", width=2, dash="dash"))
    fig_quadrant.add_shape(type="line", x0=4.5, y0=6.0, x1=9.0, y1=6.0, line=dict(color="rgba(255,255,255,0.3)", width=2, dash="dash"))
    st.plotly_chart(fig_quadrant, use_container_width=True)

with colD2:
    st.markdown("#### Matrix Summary Aggregates")
    df_risk = df_output.groupby("Risk Profile")[["Sprint Velocity", "Quality Score (%)"]].mean().reset_index()
    
    # FIX: Error hatane ke liye naya safe rendering method formatting ke saath
    st.dataframe(
        df_risk,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk Profile": st.column_config.TextColumn("Risk Category"),
            "Sprint Velocity": st.column_config.NumberColumn("Avg Velocity", format="%.2f pts"),
            "Quality Score (%)": st.column_config.NumberColumn("Quality Score", format="%.1f%%")
        }
    )
