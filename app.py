# app.py
import streamlit as st
from main import AutomatedEDA
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.validators import DataValidator
from src.risk_engine import RiskEngine
from src.report_generator import ReportGenerator
import os

def clean_dataframe_for_display(df):
    """
    Clean dataframe to make it compatible with PyArrow/Streamlit display.
    Converts problematic object columns to strings.
    """
    df_display = df.copy()
    
    # Convert all object columns to string to avoid PyArrow issues
    for col in df_display.columns:
        if df_display[col].dtype == 'object':
            df_display[col] = df_display[col].astype(str)
    
    return df_display

st.title("DataQA (Quality Assurance) Tool")

# File upload
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv","xlsx"])

if uploaded_file:
    source_type = "csv" if uploaded_file.name.endswith(".csv") else "excel"
    
    # Save and load data
    with open(f"temp_{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    eda = AutomatedEDA(data_source=f"temp_{uploaded_file.name}", source_type=source_type)
    df = eda.load_data()
    
    # Run validations
    validator = DataValidator(df)
    issues = validator.run_all_validations()
    
    # Calculate risk
    risk_engine = RiskEngine()
    risk_score = risk_engine.calculate_risk(issues, df)

    # Dataset overview
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Duplicates", df.duplicated().sum())
    with col4:
        st.metric("Risk Level", risk_score.risk_level)
    
    st.dataframe(clean_dataframe_for_display(df.head(10)))
    
    # Risk Assessment Section - NEW!
    st.subheader("Data Quality Risk Assessment")
    
    # Risk score display
    risk_col1, risk_col2, risk_col3 = st.columns(3)
    with risk_col1:
        # Display as integer if it's a whole number, otherwise show decimal
        score_display = int(risk_score.total_score) if risk_score.total_score % 1 == 0 else risk_score.total_score
        st.metric("Risk Score", f"{score_display}/100")
    with risk_col2:
        st.metric("Total Issues", risk_score.issue_count)
    with risk_col3:
        st.metric("High Severity", risk_score.high_severity_count)
    
    # Risk recommendations
    if risk_score.recommendations:
        st.write("**Recommendations:**")
        for rec in risk_score.recommendations:
            st.info(rec)
    
    # Issues breakdown
    if issues:
        st.write("**Issues Found:**")
        
        # Show issue summary by type
        issue_summary = {}
        for issue in issues:
            issue_type = issue.check_type
            if issue_type not in issue_summary:
                issue_summary[issue_type] = {'count': 0, 'severity': {}}
            issue_summary[issue_type]['count'] += 1
            severity = issue.severity
            issue_summary[issue_type]['severity'][severity] = issue_summary[issue_type]['severity'].get(severity, 0) + 1
        
        # Display summary
        st.write("**Issue Summary by Type:**")
        summary_data = []
        for issue_type, data in issue_summary.items():
            summary_data.append({
                'Issue Type': issue_type.replace('_', ' ').title(),
                'Count': data['count'],
                'High': data['severity'].get('HIGH', 0),
                'Medium': data['severity'].get('MEDIUM', 0),
                'Low': data['severity'].get('LOW', 0)
            })
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(clean_dataframe_for_display(summary_df))
        
        # Show detailed issues with expander
        with st.expander("View Detailed Issues"):
            issues_data = []
            for issue in issues:
                issues_data.append({
                    'Severity': issue.severity,
                    'Check Type': issue.check_type,
                    'Column': issue.column if issue.column else 'N/A',
                    'Message': issue.message
                })
            issues_df = pd.DataFrame(issues_data)
            st.dataframe(clean_dataframe_for_display(issues_df))
    else:
        st.success("No data quality issues found!")

    # Basic statistics
    st.subheader("Summary Statistics")
    st.dataframe(clean_dataframe_for_display(df.describe()))

    # Data quality
    st.subheader("Data Quality")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Missing Values**")
        missing_df = df.isna().sum().to_frame(name='Missing Count')
        st.dataframe(clean_dataframe_for_display(missing_df))
    with col2:
        st.write("**Data Types**")
        dtypes_df = df.dtypes.to_frame(name='Data Type')
        st.dataframe(clean_dataframe_for_display(dtypes_df))

    # CORRELATION HEATMAP - The main visualization!
    st.subheader("Correlation Heatmap")
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0, ax=ax)
        st.pyplot(fig)
        plt.close()
    else:
        st.warning("No numeric columns to correlate")

    # Export
    st.subheader("Export Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate Excel Report"):
            eda.export_summary(excel_path="EDA_Summary.xlsx")
            st.success("Excel report saved: EDA_Summary.xlsx")
            with open("EDA_Summary.xlsx", "rb") as f:
                st.download_button("Download Excel Report", f, "EDA_Summary.xlsx")
    
    with col2:
        if st.button("Generate Full Validation Report"):
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs", exist_ok=True)
            
            # Generate all reports
            reporter = ReportGenerator(df, issues, risk_score)
            reporter.generate_all_reports(output_dir="outputs")
            
            # Save risk summary
            risk_engine.export_risk_summary(risk_score, issues, "outputs/risk_summary.txt")
            
            st.success("Validation reports generated!")
            
            # Provide download buttons
            with open("outputs/validation_report.html", "rb") as f:
                st.download_button("Download HTML Report", f, "validation_report.html", mime="text/html")
            
            with open("outputs/risk_summary.txt", "rb") as f:
                st.download_button("Download Risk Summary", f, "risk_summary.txt", mime="text/plain")
