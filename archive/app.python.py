import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Advanced Health & Wellness Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. DATA LOADING LAYERS (CACHED)
# ==============================================================================
@st.cache_data(show_spinner="Parsing dataset...")
def load_data(file_source):
    """
    Safely parses incoming data assets into a unified pandas DataFrame context.
    """
    try:
        return pd.read_csv(file_source)
    except Exception as e:
        st.error(f"Error parsing data file structure: {e}")
        return None

# ==============================================================================
# 3. UI LAYOUT BUILDER
# ==============================================================================
def render_header():
    st.title("🏥 Enterprise Health & Wellness Analytics Platform")
    st.markdown(
        """
        *An interactive, high-fidelity data engine built to examine correlations 
        between biometric profiles, environmental stressors, and occupational output metrics.*
        """
    )
    st.write("---")

# ==============================================================================
# 4. MAIN APPLICATION CORE
# ==============================================================================
def main():
    render_header()
    
    # Sidebar Setup
    st.sidebar.header("📁 Data Administration")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Health CSV File", 
        type=["csv"],
        help="Provide your 'early_wakeup_health_dataset_cleaned.csv' structure here."
    )
    
    df = None

    # Ingestion Logic Engine (Uploaded File -> Local File -> Auto-Matching Search -> Graceful Warning Window)
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.sidebar.success("✅ Custom session database compiled.")
    else:
        local_path = "early_wakeup_health_dataset_cleaned.csv"
        
        if os.path.exists(local_path):
            df = load_data(local_path)
            st.sidebar.info("ℹ️ Production local dataset loaded automatically.")
        else:
            # Look for file anomalies or hidden system extensions inside current path focus
            directory_files = os.listdir('.')
            matched_files = [f for f in directory_files if 'early_wakeup' in f.lower()]
            
            if matched_files:
                df = load_data(matched_files[0])
                st.sidebar.info(f"ℹ️ Auto-matched localized asset: {matched_files[0]}")
            else:
                st.sidebar.warning("⚠️ Critical Data Source Missing.")
                st.info("👋 System waiting for data. Please drop 'early_wakeup_health_dataset_cleaned.csv' into the sidebar module to populate graphs.")
                st.stop()

    # Active Execution Layer
    if df is not None:
        
        # ----------------------------------------------------------------------
        # GLOBAL SIDEBAR FILTERS
        # ----------------------------------------------------------------------
        st.sidebar.write("---")
        st.sidebar.header("🔍 Global Segments")
        
        # Age Slider Constraint
        if 'Age' in df.columns:
            min_age = int(df['Age'].min())
            max_age = int(df['Age'].max())
            selected_age = st.sidebar.slider("Age Window", min_age, max_age, (min_age, max_age))
            df = df[(df['Age'] >= selected_age[0]) & (df['Age'] <= selected_age[1])]

        # Gender Segment Filter
        if 'Gender' in df.columns:
            genders = df['Gender'].dropna().unique().tolist()
            selected_genders = st.sidebar.multiselect("Gender Matrix", options=genders, default=genders)
            df = df[df['Gender'].isin(selected_genders)]
            
        # Occupation Segment Filter
        if 'Occupation' in df.columns:
            occupations = df['Occupation'].dropna().unique().tolist()
            # Select the top 4 jobs by default to avoid a crowded initial chart render
            default_occupations = occupations[:4] if len(occupations) >= 4 else occupations
            selected_occ = st.sidebar.multiselect("Occupation Segment", options=occupations, default=default_occupations)
            if selected_occ:
                df = df[df['Occupation'].isin(selected_occ)]

        # ----------------------------------------------------------------------
        # EXECUTIVE BIOMARKERS SUMMARY (KPI CARDS)
        # ----------------------------------------------------------------------
        st.subheader("📌 Key Biomarkers & Core Indicators")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            if 'Sleep_Duration_Hours' in df.columns:
                avg_sleep = df['Sleep_Duration_Hours'].mean()
                st.metric(label="Avg Sleep Duration", value=f"{avg_sleep:.1f} Hrs")
                
        with kpi2:
            if 'Health_Score' in df.columns:
                avg_health = df['Health_Score'].mean()
                st.metric(label="Global Health Index", value=f"{avg_health:.1f} / 100")
                
        with kpi3:
            if 'Stress_Level' in df.columns:
                avg_stress = df['Stress_Level'].mean()
                st.metric(label="Perceived Stress Average", value=f"{avg_stress:.1f} / 10")
                
        with kpi4:
            if 'Daily_Steps' in df.columns:
                avg_steps = df['Daily_Steps'].mean()
                st.metric(label="Daily Physical Steps", value=f"{int(avg_steps):,}")

        st.write("---")
        
        # ----------------------------------------------------------------------
        # ANALYTICS GRID 1: PHYSICAL METRICS & SLEEP BEHAVIORS
        # ----------------------------------------------------------------------
        st.subheader("📊 Primary Behavioral Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Physical Profiles: BMI vs. Activity Output")
            if 'BMI' in df.columns and 'Daily_Steps' in df.columns:
                fig_scatter = px.scatter(
                    df, 
                    x='BMI', 
                    y='Daily_Steps', 
                    color='Gender' if 'Gender' in df.columns else None,
                    size='Age' if 'Age' in df.columns else None,
                    labels={'Daily_Steps': 'Steps Logged', 'BMI': 'Body Mass Index (BMI)'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
                
        with col2:
            st.markdown("#### Sleep Consistency: Night Awakenings Variance")
            if 'Number_of_Night_Awakenings' in df.columns:
                # Fallback to alternate segmentation column if 'Wellness_Category' isn't clean
                color_target = 'Wellness_Category' if 'Wellness_Category' in df.columns else ('Gender' if 'Gender' in df.columns else None)
                fig_box = px.box(
                    df, 
                    x='Early_Waker' if 'Early_Waker' in df.columns else 'Gender', 
                    y='Number_of_Night_Awakenings',
                    color=color_target,
                    labels={'Number_of_Night_Awakenings': 'Disruption Events', 'Early_Waker': 'Early Waker Status'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_box, use_container_width=True)

        st.write("---")

        # ----------------------------------------------------------------------
        # ANALYTICS GRID 2: MENTAL HYGIENE & OCCUPATIONAL CORRELATIONS
        # ----------------------------------------------------------------------
        st.subheader("🧠 Mental Well-being & Occupational Matrix")
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### Digital Load: Pre-Bed Screen Time Impact on Stress")
            if 'Screen_Time_Before_Bed_Hours' in df.columns and 'Stress_Level' in df.columns:
                fig_trend = px.scatter(
                    df,
                    x='Screen_Time_Before_Bed_Hours',
                    y='Stress_Level',
                    trendline="ols",
                    labels={'Screen_Time_Before_Bed_Hours': 'Screen Usage (Hours)', 'Stress_Level': 'Stress Level (1-10)'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_trend, use_container_width=True)
                
        with col4:
            st.markdown("#### Operational Load: Daily Working Hours Matrix")
            if 'Occupation' in df.columns and 'Working_Hours_Per_Day' in df.columns:
                job_df = df.groupby('Occupation')['Working_Hours_Per_Day'].mean().reset_index()
                fig_bar = px.bar(
                    job_df,
                    x='Working_Hours_Per_Day',
                    y='Occupation',
                    orientation='h',
                    color='Working_Hours_Per_Day',
                    color_continuous_scale=px.colors.sequential.Plotly3,
                    labels={'Working_Hours_Per_Day': 'Avg Daily Working Hours'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        # ----------------------------------------------------------------------
        # DATA MATRIX DETAILED EXPANSION
        # ----------------------------------------------------------------------
        st.write("---")
        if st.checkbox("Expand Corporate Cleaned Operational Ledger"):
            st.subheader("Active Operational Query Subset")
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
