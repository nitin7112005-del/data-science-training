import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Health & Wellness Dashboard", layout="wide")
st.title("🏥 Personal Health & Wellness Dashboard")

# --- SIDEBAR FILE UPLOADER ---
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Apni CSV file yahan drag-and-drop ya browse karein", type=["csv"])

# Data load karne ka naya logic
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Agar file upload nahi hui toh purana tareeka automatic dhoondhne ka try karega
    try:
        df = pd.read_csv("early_wakeup_health_dataset_cleaned.csv")
        st.sidebar.success("Folder se automatic file mil gayi!")
    except FileNotFoundError:
        st.info("👋 Dashboard shuru karne ke liye sidebar mein 'early_wakeup_health_dataset_cleaned.csv' file upload karein.")
        st.stop() # Jab tak file nahi aayegi, aage ka code nahi chalega

# --- Iske neeche aapka baaki ka saara filter aur charts ka code same rahega ---
