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
# 2. DATA LOADING LAYERS
# ==============================================================================
@st.cache_data(show_spinner="Parsing dataset...")
def load_data(file_source):
    try:
        return pd.read_csv(file_source)
    except Exception as e:
        st.error(f"Error parsing data file: {e}")
        return None

def generate_default_data():
    """Generates an enterprise-safe fallback dataset to prevent blank screens."""
    import numpy as np
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=150, freq='D')
    return pd.DataFrame({
        "Age": np.random.randint(20, 65, size=150),
        "Gender": np.random.choice(["Male", "Female"], size=150),
        "Early_Waker": np.random.choice(["Yes", "No"], size=150),
        "Sleep_Duration_Hours": np.random.uniform(5.5, 8.5, size=150),
        "Health_Score": np.random.randint(55, 95, size=150),
        "Stress_Level": np.random.uniform(3.0, 8.5, size=150),
        "Daily_Steps": np.random.randint(3000, 12000, size=150),
        "Exercise_Type": np.random.choice(["Running", "HIIT", "Yoga", "Gym"], size=150),
        "Energy_Level_Score": np.random.uniform(4.0, 9.0, size=150),
        "Wellness_Category": np.random.choice(["Good", "Excellent", "Fair"], size=150)
    })

# ==============================================================================
# 3. UI LAYOUT BUILDER
# ==============================================================================
def render_header():
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
        help="Upload 'early_wakeup_health_dataset_cleaned.csv' to visualize custom metrics."
    )
    
    df = None

    # Ingestion Flow
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.sidebar.success("✅ File uploaded successfully.")
    else:
        import os
        if os.path.exists("early_wakeup_health_dataset_cleaned.csv"):
            df = load_data("early_wakeup_health_dataset_cleaned.csv")
            st.sidebar.info("ℹ️ Using default local dataset.")
        else:
            df = generate_default_data()
            st.sidebar.warning("⚠️ CSV not detected. Displaying demonstration dataset.")

    # Render Dashboard Components
    if df is not None:
        
        # ----------------------------------------------------------------------
        # GLOBAL FILTERS
        # ----------------------------------------------------------------------
        st.sidebar.write("---")
        st.sidebar.header("🔍 Global Filters")
        
        if 'Gender' in df.columns:
            genders = df['Gender'].dropna().unique().tolist()
            selected_genders = st.sidebar.multiselect("Gender", options=genders, default=genders)
            df = df[df['Gender'].isin(selected_genders)]
            
        if 'Early_Waker' in df.columns:
            waker_options = df['Early_Waker'].dropna().unique().tolist()
            selected_wakers = st.sidebar.multiselect("Early Waker Status", options=waker_options, default=waker_options)
            df = df[df['Early_Waker'].isin(selected_wakers)]
            
        # ----------------------------------------------------------------------
        # KEY PERFORMANCE INDICATORS
        # ----------------------------------------------------------------------
        st.subheader("📌 Key Performance Indicators")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            if 'Sleep_Duration_Hours' in df.columns:
                avg_sleep = df['Sleep_Duration_Hours'].mean()
                st.metric(label="Avg Sleep Duration", value=f"{avg_sleep:.1f} Hrs")
                
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
        # METRIC VISUALIZATIONS
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
        # DETAILED MATRIX VIEW
        # ----------------------------------------------------------------------
        st.write("---")
        if st.checkbox("Show Screened Raw Dataset View"):
            st.subheader("Filtered Dataset Overview")
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
