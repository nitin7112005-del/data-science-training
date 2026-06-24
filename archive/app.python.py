import streamlit as st
import pandas as pd
import plotly.express as px

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
# 2. DATA LOADING LAYERS
# ==============================================================================
@st.cache_data(show_spinner="Parsing enterprise dataset...")
def load_data(file_source):
    try:
        return pd.read_csv(file_source)
    except Exception as e:
        st.error(f"Error parsing data file: {e}")
        return None

# ==============================================================================
# 3. MAIN DASHBOARD EXECUTION
# ==============================================================================
def main():
    st.title("🏥 Enterprise Health & Wellness Analytics Platform")
    st.markdown("*A deep-dive analytical view into personal biomarkers, lifestyle choices, and productivity correlations.*")
    st.write("---")
    
    # Sidebar Setup
    st.sidebar.header("📁 Data Administration")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Health CSV File", 
        type=["csv"],
        help="Upload 'early_wakeup_health_dataset_cleaned.csv' to populate metrics."
    )
    
    df = None

    # Ingestion Layer
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        import os
        if os.path.exists("early_wakeup_health_dataset_cleaned.csv"):
            df = load_data("early_wakeup_health_dataset_cleaned.csv")
            st.sidebar.info("ℹ️ Using default local database.")
        else:
            st.sidebar.warning("⚠️ Critical Data Source Missing.")
            st.info("👋 Please upload your data file in the sidebar to populate metrics.")
            st.stop()

    if df is not None:
        # ----------------------------------------------------------------------
        # ADVANCED SIDEBAR FILTERS
        # ----------------------------------------------------------------------
        st.sidebar.write("---")
        st.sidebar.header("🔍 Demographic & Lifestyle Filters")
        
        # Age Slider Filter
        if 'Age' in df.columns:
            min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
            selected_age = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))
            df = df[(df['Age'] >= selected_age[0]) & (df['Age'] <= selected_age[1])]

        # Gender Filter
        if 'Gender' in df.columns:
            genders = df['Gender'].dropna().unique().tolist()
            selected_genders = st.sidebar.multiselect("Gender", options=genders, default=genders)
            df = df[df['Gender'].isin(selected_genders)]
            
        # Occupation Filter
        if 'Occupation' in df.columns:
            occupations = df['Occupation'].dropna().unique().tolist()
            selected_occ = st.sidebar.multiselect("Occupation", options=occupations, default=occupations[:3])
            if selected_occ:
                df = df[df['Occupation'].isin(selected_occ)]

        # ----------------------------------------------------------------------
        # EXECUTIVE SUMMARY (KPI CARDS)
        # ----------------------------------------------------------------------
        st.subheader("📌 Key Biomarkers & Core Indicators")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            avg_sleep = df['Sleep_Duration_Hours'].mean() if 'Sleep_Duration_Hours' in df.columns else 0
            st.metric(label="Avg Sleep Duration", value=f"{avg_sleep:.1f} Hrs", delta_color="normal")
                
        with kpi2:
            avg_health = df['Health_Score'].mean() if 'Health_Score' in df.columns else 0
            st.metric(label="Global Health Score", value=f"{avg_health:.1f} / 100")
                
        with kpi3:
            avg_stress = df['Stress_Level'].mean() if 'Stress_Level' in df.columns else 0
            st.metric(label="Perceived Stress Matrix", value=f"{avg_stress:.1f} / 10")
                
        with kpi4:
            avg_screen = df['Screen_Time_Before_Bed_Hours'].mean() if 'Screen_Time_Before_Bed_Hours' in df.columns else 0
            st.metric(label="Bedtime Screen Time", value=f"{avg_screen:.1f} Hrs", delta="-0.5 Hrs")

        st.write("---")
        
        # ----------------------------------------------------------------------
        # ANALYTICS GRID 1: LIFESTYLE & BIOMARKERS
        # ----------------------------------------------------------------------
        st.subheader("📊 Primary Behavioral Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Physical Metrics: BMI vs. Physical Activity")
            if 'BMI' in df.columns and 'Daily_Steps' in df.columns:
                fig_scatter1 = px.scatter(
                    df, 
                    x='BMI', 
                    y='Daily_Steps', 
                    color='Gender' if 'Gender' in df.columns else None,
                    size='Age' if 'Age' in df.columns else None,
                    labels={'Daily_Steps': 'Steps Walked Daily', 'BMI': 'Body Mass Index (BMI)'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_scatter1, use_container_width=True)
                
        with col2:
            st.markdown("#### Sleep Disturbance: Night Awakenings by Age Segment")
            if 'Age' in df.columns and 'Number_of_Night_Awakenings' in df.columns:
                fig_box = px.box(
                    df, 
                    x='Gender' if 'Gender' in df.columns else 'Age', 
                    y='Number_of_Night_Awakenings',
                    color='Early_Waker' if 'Early_Waker' in df.columns else None,
                    labels={'Number_of_Night_Awakenings': 'Night Awakenings'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_box, use_container_width=True)

        st.write("---")

        # ----------------------------------------------------------------------
        # ANALYTICS GRID 2: MENTAL HEALTH & WORKPLACE CORRELATIONS
        # ----------------------------------------------------------------------
        st.subheader("🧠 Mental Well-being & Occupational Matrix")
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### Digital Load: Bedtime Screen Time vs. Stress Levels")
            if 'Screen_Time_Before_Bed_Hours' in df.columns and 'Stress_Level' in df.columns:
                fig_trend = px.scatter(
                    df,
                    x='Screen_Time_Before_Bed_Hours',
                    y='Stress_Level',
                    trendline="ols",
                    labels={'Screen_Time_Before_Bed_Hours': 'Screen Time (Hrs)', 'Stress_Level': 'Stress Index'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_trend, use_container_width=True)
                
        with col4:
            st.markdown("#### Occupational Strain: Average Working Hours & Anxiety Profile")
            if 'Occupation' in df.columns and 'Working_Hours_Per_Day' in df.columns:
                job_df = df.groupby('Occupation')[['Working_Hours_Per_Day', 'Health_Score']].mean().reset_index()
                fig_bar2 = px.bar(
                    job_df,
                    x='Working_Hours_Per_Day',
                    y='Occupation',
                    orientation='h',
                    color='Health_Score',
                    color_continuous_scale=px.colors.sequential.Viridis,
                    labels={'Working_Hours_Per_Day': 'Avg Daily Working Hours'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_bar2, use_container_width=True)

        # ----------------------------------------------------------------------
        # DETAILED MASTER MATRIX VIEW
        # ----------------------------------------------------------------------
        st.write("---")
        if st.checkbox("Expand Corporate Cleaned Dataset Ledger"):
            st.subheader("Filtered Operational Database")
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
