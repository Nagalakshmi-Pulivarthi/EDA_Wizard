# app.py
# app.py
import streamlit as st
from main import AutomatedEDA
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Automated EDA Tool")

# File upload
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv","xlsx"])

if uploaded_file:
    source_type = "csv" if uploaded_file.name.endswith(".csv") else "excel"
    
    # Save and load data
    with open(f"temp_{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    eda = AutomatedEDA(data_source=f"temp_{uploaded_file.name}", source_type=source_type)
    df = eda.load_data()

    # Dataset overview
    st.subheader("📊 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Duplicates", df.duplicated().sum())
    
    st.dataframe(df.head(10))

    # Basic statistics
    st.subheader("📈 Summary Statistics")
    st.dataframe(df.describe())

    # Data quality
    st.subheader("🔍 Data Quality")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Missing Values**")
        st.dataframe(df.isna().sum())
    with col2:
        st.write("**Data Types**")
        st.dataframe(df.dtypes)

    # CORRELATION HEATMAP - The main visualization!
    st.subheader(" 🔥Correlation Heatmap")
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0, ax=ax)
        st.pyplot(fig)
        plt.close()
    else:
        st.warning("No numeric columns to correlate")

    # Export
    st.subheader("💾 Export Report")
    if st.button("Generate Excel Report"):
        eda.export_summary(excel_path="EDA_Summary.xlsx")
        st.success("✅ Excel report saved: EDA_Summary.xlsx")
        with open("EDA_Summary.xlsx", "rb") as f:
            st.download_button("⬇️ Download Excel Report", f, "EDA_Summary.xlsx")