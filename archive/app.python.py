import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Health & Wellness Dashboard", layout="wide")

st.title("🏥 Personal Health & Wellness Dashboard")
st.markdown("Is dashboard ke zariye aap sleep, exercise, aur mental health ke correlations ko analyze kar sakte hain.")
st.write("---")

# 2. Data Load karna
@st.cache_data
def load_data():
    # File ka sahi naam jo aapne upload kiya hai
    df = pd.read_csv("early_wakeup_health_dataset_cleaned.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'early_wakeup_health_dataset_cleaned.csv' file nahi mili. Kripya check karein ki file aapke project folder mein hi ho.")
    st.stop()

# 3. Sidebar Filters
st.sidebar.header("🔍 Filters")

# Gender Filter
all_genders = df["Gender"].dropna().unique().tolist()
selected_gender = st.sidebar.multiselect("Gender select karein:", options=all_genders, default=all_genders)

# Early Waker Filter
all_wakers = df["Early_Waker"].dropna().unique().tolist()
selected_waker = st.sidebar.multiselect("Early Waker? (Subah jaldi uthne wale):", options=all_wakers, default=all_wakers)

# Country Filter (Top 10 ya saare)
all_countries = df["Country"].dropna().unique().tolist()
selected_countries = st.sidebar.multiselect("Country select karein:", options=all_countries, default=all_countries[:5]) # Default top 5

# Data ko filter karna
filtered_df = df[
    (df["Gender"].isin(selected_gender)) & 
    (df["Early_Waker"].isin(selected_waker)) &
    (df["Country"].isin(selected_countries))
]

# 4. KPI Metrics (Top Cards)
st.subheader("📌 Key Health Metrics (Filtered)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    avg_sleep = filtered_df["Sleep_Duration_Hours"].mean()
    st.metric(label="Avg Sleep Duration 😴", value=f"{avg_sleep:.1f} Hours" if not pd.isna(avg_sleep) else "N/A")

with kpi2:
    avg_health = filtered_df["Health_Score"].mean()
    st.metric(label="Avg Health Score ❤️", value=f"{avg_health:.1f}/100" if not pd.isna(avg_health) else "N/A")

with kpi3:
    avg_stress = filtered_df["Stress_Level"].mean()
    st.metric(label="Avg Stress Level 🧠", value=f"{avg_stress:.1f}/10" if not pd.isna(avg_stress) else "N/A")

with kpi4:
    avg_steps = filtered_df["Daily_Steps"].mean()
    st.metric(label="Avg Daily Steps 👣", value=f"{int(avg_steps):,}" if not pd.isna(avg_steps) else "N/A")

st.write("---")

# 5. Visualizations / Charts
st.subheader("📊 Data Visualizations")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏃‍♂️ Exercise Type vs Energy Level")
    if "Exercise_Type" in filtered_df.columns and "Energy_Level_Score" in filtered_df.columns:
        # Grouping data for better chart
        exercise_df = filtered_df.groupby("Exercise_Type")["Energy_Level_Score"].mean().reset_index()
        fig_bar = px.bar(exercise_df, x="Exercise_Type", y="Energy_Level_Score", 
                         labels={"Energy_Level_Score": "Avg Energy Level"},
                         color="Exercise_Type", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Exercise_Type ya Energy_Level_Score column nahi mila.")

with col2:
    st.markdown("#### 💤 Sleep Duration vs Health Score")
    if "Sleep_Duration_Hours" in filtered_df.columns and "Health_Score" in filtered_df.columns:
        fig_scatter = px.scatter(filtered_df, x="Sleep_Duration_Hours", y="Health_Score", 
                                 color="Wellness_Category", trendline="ols",
                                 labels={"Sleep_Duration_Hours": "Sleep (Hours)", "Health_Score": "Health Score"})
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Sleep ya Health Score column missing hai.")

# 6. Stress Level by Occupation
st.write("---")
st.markdown("#### 💼 Stress Level by Occupation")
if "Occupation" in filtered_df.columns and "Stress_Level" in filtered_df.columns:
    occ_stress = filtered_df.groupby("Occupation")["Stress_Level"].mean().sort_values(ascending=False).reset_index()
    fig_occ = px.bar(occ_stress, x="Stress_Level", y="Occupation", orientation='h',
                     color="Stress_Level", color_continuous_scale="Reds",
                     labels={"Stress_Level": "Avg Stress Level"})
    st.plotly_chart(fig_occ, use_container_width=True)

# 7. Raw Data
st.write("---")
if st.checkbox("Filtered Data Ki Detail Table Dekhein"):
    st.dataframe(filtered_df)