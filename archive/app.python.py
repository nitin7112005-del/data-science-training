import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Health & Wellness Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CACHED DATA LOADING
# ==============================================================================
@st.cache_data(show_spinner="Loading dataset...")
def load_data(file_source):
    """
    Safely reads a CSV file and handles unexpected parser errors.
    """
    try:
        return pd.read_csv(file_source)
    except Exception as e:
        st.error(f"Error parsing data file: {e}")
        return None

# ==============================================================================
# 3. UI RENDERING COMPONENTS
# ==============================================================================
def render_header():
    """
    Renders the primary application headers and overview markdown.
    """
    st.title("🏥 Personal Health & Wellness Dashboard")
    st.markdown(
        """
        *An interactive analytics platform to explore correlations between 
        sleep hygiene, exercise patterns, daily habits, and overall health scores.*
        """
    )
    st.write("---")

# ==============================================================================
# 4. MAIN DASHBOARD EXECUTION
# ==============================================================================
def main():
    render_header()
    
    # Sidebar Configuration
    st.sidebar.header("📁 Data Management")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Health CSV File", 
        type=["csv"],
        help="Provide the 'early_wakeup_health_dataset_cleaned.csv' file here."
    )
    
    df = None

    # Data Ingestion Hierarchy (Uploaded File -> Local Fallback -> Graceful Stop)
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.sidebar.success("✅ File uploaded successfully.")
    else:
        try:
            df = load_data("early_wakeup_health_dataset_cleaned.csv")
            st.sidebar.info("ℹ️ Using default local dataset.")
        except FileNotFoundError:
            st.warning("⚠️ Data source could not be resolved automatically.")
            st.info("👋 Please upload your 'early_wakeup_health_dataset_cleaned.csv' file via the sidebar to initialize the dashboard.")
            st.stop()

    # Active Dashboard Session
    if df is not None:
        
        # ----------------------------------------------------------------------
        # SIDEBAR FILTERS SECTION
        # ----------------------------------------------------------------------
        st.sidebar.write("---")
        st.sidebar.header("🔍 Global Filters")
        
        # Dynamic Filter: Gender
        if 'Gender' in df.columns:
            genders = df['Gender'].dropna().unique().tolist()
            selected_genders = st.sidebar.multiselect("Gender", options=genders, default=genders)
            df = df[df['Gender'].isin(selected_genders)]
            
        # Dynamic Filter: Early Waker Status
        if 'Early_Waker' in df.columns:
            waker_options = df['Early_Waker'].dropna().unique().tolist()
            selected_wakers = st.sidebar.multiselect("Early Waker Status", options=waker_options, default=waker_options)
            df = df[df['Early_Waker'].isin(selected_wakers)]
            
        # ----------------------------------------------------------------------
        # MAIN DASHBOARD METRICS & KPI CARDS
        # ----------------------------------------------------------------------
        st.subheader("📌 Key Performance Indicators")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            if 'Sleep_Duration_Hours' in df.columns:
                avg_sleep = df['Sleep_Duration_Hours'].mean()
                st.metric(label="Avg Sleep Duration", value=f"{avg_sleep:.2f} Hrs")
                
        with kpi2:
            if 'Health_Score' in df.columns:
                avg_health = df['Health_Score'].mean()
                st.metric(label="Avg Health Score", value=f"{avg_health:.1f} / 100")
                
        with kpi3:
            if 'Stress_Level' in df.columns:
                avg_stress = df['Stress_Level'].mean()
                st.metric(label="Avg Stress Level", value=f"{avg_stress:.1f} / 10")
                
        with kpi4:
            if 'Daily_Steps' in df.columns:
                avg_steps = df['Daily_Steps'].mean()
                st.metric(label="Avg Daily Steps", value=f"{int(avg_steps):,}")

        st.write("---")
        
        # ----------------------------------------------------------------------
        # VISUALIZATIONS SECTION
        # ----------------------------------------------------------------------
        st.subheader("📊 Data Visualizations")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Exercise Type vs. Energy Level")
            if 'Exercise_Type' in df.columns and 'Energy_Level_Score' in df.columns:
                exercise_df = df.groupby('Exercise_Type')['Energy_Level_Score'].mean().reset_index()
                fig_bar = px.bar(
                    exercise_df, 
                    x='Exercise_Type', 
                    y='Energy_Level_Score',
                    labels={'Energy_Level_Score': 'Avg Energy Level'},
                    color='Exercise_Type',
                    template="plotly_white"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with col2:
            st.markdown("#### Sleep Duration vs. Health Score")
            if 'Sleep_Duration_Hours' in df.columns and 'Health_Score' in df.columns:
                fig_scatter = px.scatter(
                    df, 
                    x='Sleep_Duration_Hours', 
                    y='Health_Score', 
                    color='Wellness_Category' if 'Wellness_Category' in df.columns else None,
                    labels={'Sleep_Duration_Hours': 'Sleep (Hours)', 'Health_Score': 'Health Score'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

        # ----------------------------------------------------------------------
        # DETAILED DATA TABLE VIEW
        # ----------------------------------------------------------------------
        st.write("---")
        if st.checkbox("Show Screened Raw Dataset View"):
            st.subheader("Filtered Dataset Overview")
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
