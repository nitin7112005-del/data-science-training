import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page & Aesthetic Configurations
st.set_page_config(
    page_title="Enterprise Health & Wellness Analytics Engine",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean, corporate data engine look
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #1E3A8A; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar - Module Input
st.sidebar.header("📥 Data Management Module")
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(
    "Drop 'early_wakeup_health_dataset_cleaned.csv' here", 
    type=["csv"],
    help="Upload the official cleaned enterprise dataset."
)

# 3. App Header Frame
st.title("🏥 Enterprise Health & Wellness Analytics Platform")
st.markdown("### High-Fidelity Data Engine: Biometrics, Stressors, and Occupational Output")
st.markdown("---")

# 4. Core Processing Logic
if uploaded_file is not None:
    @st.cache_data
    def load_and_preprocess(file):
        return pd.read_csv(file)

    try:
        df = load_and_preprocess(uploaded_file)
        
        # --- SIDEBAR COHORT FILTERS ---
        st.sidebar.subheader("🎛️ Cohort Filtering Engine")
        
        # Gender Filter
        unique_genders = df['Gender'].unique().tolist()
        gender_filter = st.sidebar.multiselect("Gender Focus:", options=unique_genders, default=unique_genders)
        
        # Early Waker Circadian Filter
        unique_wakers = df['Early_Waker'].unique().tolist()
        early_waker_filter = st.sidebar.multiselect("Circadian Profile (Early Waker):", options=unique_wakers, default=unique_wakers)
        
        # Apply Filters Dynamically
        filtered_df = df[
            (df['Gender'].isin(gender_filter)) & 
            (df['Early_Waker'].isin(early_waker_filter))
        ]
        
        # --- EXECUTIVE KPI BOARD ---
        st.subheader("📊 Cross-Sectional Cohort Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Observed Cohort", f"{len(filtered_df):,} Personnel")
        with col2:
            avg_prod = filtered_df['Productivity_Score'].mean() if 'Productivity_Score' in filtered_df.columns else 0
            st.metric("📈 Avg Productivity", f"{avg_prod:.2f} / 10")
        with col3:
            avg_stress = filtered_df['Stress_Level'].mean() if 'Stress_Level' in filtered_df.columns else 0
            st.metric("⚡ Avg Stress Index", f"{avg_stress:.2f} / 10")
        with col4:
            avg_sleep = filtered_df['Sleep_Duration_Hours'].mean() if 'Sleep_Duration_Hours' in filtered_df.columns else 0
            st.metric("💤 Sleep Baseline", f"{avg_sleep:.1f} Hrs")
            
        st.markdown("---")
        
        # --- ANALYTICAL DEEP-DIVES (TABS) ---
        tab1, tab2, tab3 = st.tabs([
            "🧬 Biometric Profiles & Biomarkers", 
            "🌪️ Environmental Stressors & Mental Matrix", 
            "💼 Occupational Output Drivers"
        ])
        
        # TAB 1: BIOMETRIC PROFILES
        with tab1:
            st.header("Cardiovascular & Biomarker Distributions")
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("Resting Heart Rate vs. Energy Scores")
                fig_biomed = px.scatter(
                    filtered_df, x="Resting_Heart_Rate", y="Energy_Level_Score",
                    color="Fitness_Level", size="Age", hover_data=["Occupation"],
                    color_discrete_sequence=px.colors.qualitative.Safe,
                    title="RHR vs. Subjective Energy Matrix"
                )
                st.plotly_chart(fig_biomed, use_container_width=True)
                
            with c2:
                st.subheader("Metabolic Distributions across Wellness Segments")
                fig_box = px.box(
                    filtered_df, x="Wellness_Category", y="Blood_Sugar_Level", 
                    color="Obesity_Risk", title="Blood Sugar Spread Across Wellness Classes",
                    color_discrete_sequence=px.colors.sequential.Bluered
                )
                st.plotly_chart(fig_box, use_container_width=True)

        # TAB 2: STRESSORS & MENTAL HEALTH
        with tab2:
            st.header("Stress, Anxiety & Cognitive Degradation Patterns")
            
            # Selectable target analysis for stress matrix
            stress_metric = st.selectbox(
                "Select Cognitive Axis for Cross-Examination:",
                ["Anxiety_Score", "Depression_Risk_Score", "Fatigue_Level_Score"]
            )
            
            fig_stress = px.density_heatmap(
                filtered_df, x="Stress_Level", y=stress_metric,
                text_auto=True, color_continuous_scale="Viridis",
                title=f"Concentration Matrix: Overall Stress Level vs. {stress_metric.replace('_', ' ')}"
            )
            st.plotly_chart(fig_stress, use_container_width=True)
            
            st.markdown("#### Lifestyle Interventions Against Mental Overhead")
            fig_line = px.box(
                filtered_df, x="Exercise_Frequency_Per_Week", y="Mood_Score",
                color="Early_Waker", title="The Impact of Activity & Early Rising on Mood Architecture"
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # TAB 3: OCCUPATIONAL OUTPUT
        with tab3:
            st.header("Predictors of Peak Human Performance")
            
            fig_output = px.scatter(
                filtered_df, x="Focus_Concentration_Score", y="Productivity_Score",
                color="Sleep_Quality_Score", size="Working_Hours_Per_Day",
                title="The Efficiency Curve: Focus vs. Productivity mapped to Sleep Quality"
            )
            st.plotly_chart(fig_output, use_container_width=True)
            
            # Cross-Correlation Matrix Subsystem
            st.subheader("🧩 Feature Interdependence Matrix")
            target_cols = [
                "Sleep_Duration_Hours", "Sleep_Quality_Score", "Screen_Time_Before_Bed_Hours",
                "Stress_Level", "Energy_Level_Score", "Productivity_Score", "Focus_Concentration_Score"
            ]
            
            # Form correlation framework from numerical layers
            corr_matrix = filtered_df[target_cols].corr()
            
            fig_heat = px.imshow(
                corr_matrix, text_auto=".2f", aspect="auto",
                color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                title="Linear Correlations: Lifestyle Factors vs. Workforce Output"
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        # 5. DATA SYSTEM EXPLORER
        with st.expander("🔍 Deep-Data Subsystem Explorer (Filtered Data Rows)"):
            st.dataframe(filtered_df)

    except Exception as e:
        st.error(f"Execution Error within Analytics Engine: {e}")
        st.info("Ensure the dataset retains all standard headers matching your workspace scheme.")

else:
    # Standby/Waiting UI Interface State
    st.info("⚙️ Core Processing Unit Idle. Waiting for 'early_wakeup_health_dataset_cleaned.csv' to initialize data streams.")
