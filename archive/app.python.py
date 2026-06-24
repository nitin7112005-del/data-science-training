import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(
    page_title="Enterprise Health & Wellness Analytics Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Sidebar - Data Input Module
st.sidebar.header("📥 Data Input Module")
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(
    "Drop 'early_wakeup_health_dataset_cleaned.csv' here", 
    type=["csv"],
    help="Upload the cleaned dataset to populate the enterprise health graphs."
)

# 3. Main Header
st.title("🏥 Enterprise Health & Wellness Analytics Platform")
st.subheader("High-fidelity data engine for biometric, environmental, and occupational output correlation.")
st.markdown("---")

# 4. Core Logic & Visualization Engine
if uploaded_file is not None:
    # Load Data
    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file)
        return df

    try:
        df = load_data(uploaded_file)
        
        # Quick-glance Metrics (KPIs)
        st.subheader("📊 Key Performance & Wellness Indicators")
        kpi1, kpi2, kpi3 = st.columns(3)
        
        # Dynamically calculate metrics if standard columns exist, otherwise fallback safely
        with kpi1:
            avg_sleep = df.select_dtypes(include=['float64', 'int64']).mean().iloc[0] if not df.empty else 0
            st.metric(label="💤 Base Sleep Metric (Avg)", value=f"{avg_sleep:.2f}")
        with kpi2:
            avg_stress = df.select_dtypes(include=['float64', 'int64']).mean().iloc[1] if len(df.columns) > 1 else 0
            st.metric(label="⚡ Environmental Stress Index (Avg)", value=f"{avg_stress:.2f}")
        with kpi3:
            avg_output = df.select_dtypes(include=['float64', 'int64']).mean().iloc[2] if len(df.columns) > 2 else 0
            st.metric(label="📈 Occupational Output (Avg)", value=f"{avg_output:.2f}")
            
        st.markdown("---")
        
        # Tabs for Analytical Deep-Dives
        tab1, tab2, tab3 = st.tabs(["🧬 Biometric Profiles", "🌪️ Environmental Stressors", "💼 Occupational Output"])
        
        with tab1:
            st.header("Biometric Distribution & Overview")
            numeric_cols = df.select_types(include=['number']).columns.tolist() if hasattr(df, 'select_types') else df.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_cols:
                bio_col = st.selectbox("Select Biometric Profile to View Distribution:", numeric_cols, key="bio_box")
                fig_hist = px.histogram(df, x=bio_col, marginal="box", box=True, color_discrete_sequence=['#4F46E5'])
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.warning("No numeric biometric data found.")
                
        with tab2:
            st.header("Stressors vs. Productivity Analytics")
            if len(numeric_cols) >= 2:
                x_axis = st.selectbox("X-Axis (e.g., Stressor/Wakeup Time):", numeric_cols, index=0)
                y_axis = st.selectbox("Y-Axis (e.g., Output/Heart Rate):", numeric_cols, index=min(1, len(numeric_cols)-1))
                
                fig_scatter = px.scatter(df, x=x_axis, y=y_axis, trendline="ols", color_discrete_sequence=['#EF4444'])
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.warning("Insufficient numeric variables to map correlations.")
                
        with tab3:
            st.header("Platform Correlation Matrix")
            if len(numeric_cols) > 1:
                corr = df[numeric_cols].corr()
                fig_heatmap = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
                st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.warning("Not enough numeric data to construct a correlation matrix.")

        # Raw Data View
        with st.expander("🔍 View Raw Analytics Data"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"An error occurred while parsing the dataset: {e}")

else:
    # Idle/Waiting State UI
    st.info("👋 System waiting for data. Please drop 'early_wakeup_health_dataset_cleaned.csv' into the sidebar module to populate graphs.")
    
    # Placeholder layout to give a sense of scale before upload
    st.image(
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=80", 
        caption="Dashboard Analytics Engine Idle State",
        use_container_width=True
    )
