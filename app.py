# app.py
import streamlit as st
from src.main import AutomatedEDA
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.validators import DataValidator
from src.risk_engine import RiskEngine
from src.report_generator import ReportGenerator
import os

# Import Plotly for interactive charts
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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


def create_interactive_plotly_charts(issues, risk_score):
    """
    Create interactive Plotly charts for the Streamlit dashboard
    """
    if not PLOTLY_AVAILABLE:
        st.warning("Plotly not installed. Install with: pip install plotly")
        return
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Risk Overview", "Issues Analysis", "Detailed Table"])
    
    with tab1:
        # Risk Score Gauge and KPIs
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk Score Gauge
            risk_score_value = risk_score.total_score if risk_score else 0
            risk_color = "red" if risk_score_value > 70 else "orange" if risk_score_value > 40 else "green"
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score_value,
                title={'text': "Risk Score", 'font': {'size': 24}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': risk_color},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 70], 'color': "lightyellow"},
                        {'range': [70, 100], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Total Issues Indicator
            fig_issues = go.Figure(go.Indicator(
                mode="number+delta",
                value=len(issues),
                title={'text': "Total Issues Found", 'font': {'size': 20}},
                delta={'reference': 0, 'increasing': {'color': "red"}},
                number={'font': {'size': 60}}
            ))
            fig_issues.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_issues, use_container_width=True)
    
    with tab2:
        if issues:
            # Collect issue details with column information
            severity_counts = {}
            type_counts = {}
            column_issues = {}  # Track issues by column
            
            for issue in issues:
                severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
                type_counts[issue.check_type] = type_counts.get(issue.check_type, 0) + 1
                
                # Track column-specific issues
                col_name = issue.column if issue.column else 'General'
                if col_name not in column_issues:
                    column_issues[col_name] = []
                column_issues[col_name].append({
                    'type': issue.check_type,
                    'severity': issue.severity,
                    'message': issue.message
                })
            
            # Create 3 charts instead of 2
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Severity bar chart with column annotations
                severity_order = ['HIGH', 'MEDIUM', 'LOW']
                severity_colors_map = {'HIGH': '#e74c3c', 'MEDIUM': '#f39c12', 'LOW': '#3498db'}
                
                # Get columns for each severity level
                severity_columns = {}
                for severity in severity_order:
                    severity_columns[severity] = set()
                
                for issue in issues:
                    col_name = issue.column if issue.column else 'General'
                    severity_columns[issue.severity].add(col_name)
                
                severities = [s for s in severity_order if s in severity_counts]
                counts = [severity_counts[s] for s in severities]
                colors = [severity_colors_map[s] for s in severities]
                
                # Create hover text with column names
                hover_texts = []
                for sev in severities:
                    cols = list(severity_columns[sev])
                    cols_text = ', '.join(cols[:5])  # Show first 5 columns
                    if len(cols) > 5:
                        cols_text += f" (+{len(cols)-5} more)"
                    hover_text = f"<b>{sev}</b><br>Count: {severity_counts[sev]}<br>Columns: {cols_text}"
                    hover_texts.append(hover_text)
                
                fig_severity = go.Figure(data=[
                    go.Bar(
                        x=severities,
                        y=counts,
                        marker_color=colors,
                        text=counts,
                        textposition='auto',
                        hovertemplate='%{customdata}<extra></extra>',
                        customdata=hover_texts
                    )
                ])
                
                # Add text annotations for HIGH severity columns
                if 'HIGH' in severities:
                    high_idx = severities.index('HIGH')
                    high_cols = list(severity_columns['HIGH'])
                    cols_label = ', '.join(high_cols[:3])  # Show first 3 columns
                    if len(high_cols) > 3:
                        cols_label += f" (+{len(high_cols)-3})"
                    
                    fig_severity.add_annotation(
                        x=high_idx,
                        y=counts[high_idx],
                        text=f"<b>{cols_label}</b>",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#e74c3c",
                        ax=40,
                        ay=-40,
                        font=dict(size=10, color="#e74c3c"),
                        bgcolor="white",
                        bordercolor="#e74c3c",
                        borderwidth=1,
                        borderpad=4
                    )
                
                fig_severity.update_layout(
                    title="Issues by Severity",
                    xaxis_title="Severity Level",
                    yaxis_title="Number of Issues",
                    height=400,
                    showlegend=False,
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                st.plotly_chart(fig_severity, use_container_width=True)
            
            with col2:
                # Issues by Column Bar Chart - NEW!
                columns = list(column_issues.keys())
                column_counts = [len(column_issues[col]) for col in columns]
                
                # Create hover text with issue details
                hover_texts = []
                for col in columns:
                    issues_list = column_issues[col]
                    hover_text = f"<b>{col}</b><br>Total Issues: {len(issues_list)}<br><br>"
                    for idx, iss in enumerate(issues_list[:3]):  # Show first 3 issues
                        hover_text += f"? {iss['type'].replace('_', ' ').title()}<br>"
                    if len(issues_list) > 3:
                        hover_text += f"<i>...and {len(issues_list) - 3} more</i>"
                    hover_texts.append(hover_text)
                
                fig_column = go.Figure(data=[
                    go.Bar(
                        x=columns,
                        y=column_counts,
                        marker_color='#9b59b6',
                        text=column_counts,
                        textposition='auto',
                        hovertemplate='%{customdata}<extra></extra>',
                        customdata=hover_texts
                    )
                ])
                fig_column.update_layout(
                    title="Issues by Column",
                    xaxis_title="Column Name",
                    yaxis_title="Number of Issues",
                    height=400,
                    showlegend=False,
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                st.plotly_chart(fig_column, use_container_width=True)
            
            with col3:
                # Issues by Type Pie Chart with column details in hover
                type_details = {}
                for col, issues_list in column_issues.items():
                    for iss in issues_list:
                        issue_type = iss['type']
                        if issue_type not in type_details:
                            type_details[issue_type] = []
                        type_details[issue_type].append(col)
                
                # Create hover text with column names
                hover_texts_pie = []
                for issue_type in type_counts.keys():
                    affected_cols = type_details.get(issue_type, [])
                    cols_text = ', '.join(affected_cols) if affected_cols else 'N/A'
                    hover_text = f"<b>{issue_type.replace('_', ' ').title()}</b><br>Count: {type_counts[issue_type]}<br>Columns: {cols_text}"
                    hover_texts_pie.append(hover_text)
                
                fig_type = go.Figure(data=[
                    go.Pie(
                        labels=[t.replace('_', ' ').title() for t in type_counts.keys()],
                        values=list(type_counts.values()),
                        hole=0.3,
                        hovertemplate='%{customdata}<extra></extra>',
                        customdata=hover_texts_pie
                    )
                ])
                fig_type.update_layout(
                    title="Issues by Type",
                    height=400,
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.success("No issues found! Your data quality is excellent.")
    
    with tab3:
        if issues:
            # Detailed Issues Table
            sorted_issues = sorted(issues, key=lambda x: ['HIGH', 'MEDIUM', 'LOW'].index(x.severity))
            
            table_data = {
                'Severity': [issue.severity for issue in sorted_issues],
                'Type': [issue.check_type.replace('_', ' ').title() for issue in sorted_issues],
                'Message': [issue.message for issue in sorted_issues],
                'Column': [issue.column or 'N/A' for issue in sorted_issues],
                'Affected Rows': [issue.row_count or 'N/A' for issue in sorted_issues]
            }
            
            # Create interactive table
            df_issues = pd.DataFrame(table_data)
            
            # Color coding function
            def color_severity(val):
                if val == 'HIGH':
                    return 'background-color: #ffcccc'
                elif val == 'MEDIUM':
                    return 'background-color: #fff4cc'
                elif val == 'LOW':
                    return 'background-color: #cce5ff'
                return ''
            
            # Apply styling
            styled_df = df_issues.style.applymap(color_severity, subset=['Severity'])
            st.dataframe(styled_df, use_container_width=True, height=400)
            
            # Download button for issues
            csv = df_issues.to_csv(index=False)
            st.download_button(
                label="Download Issues as CSV",
                data=csv,
                file_name="data_quality_issues.csv",
                mime="text/csv"
            )
        else:
            st.info("No issues to display - your data is clean!")


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
    
    # ==========================================
    # INTERACTIVE PLOTLY DASHBOARD - NEW!
    # ==========================================
    st.subheader("Interactive Data Quality Dashboard")
    st.markdown("*Explore your data quality with interactive visualizations*")
    
    create_interactive_plotly_charts(issues, risk_score)
    
    st.markdown("---")  # Separator
    # ==========================================
    
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
    
    col1, col2, col3 = st.columns(3)
    
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
    
    with col3:
        if st.button("Export Interactive Dashboard"):
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs", exist_ok=True)
            
            # Generate the Plotly dashboard
            reporter = ReportGenerator(df, issues, risk_score)
            reporter.generate_plotly_dashboard(output_path="outputs/interactive_dashboard.html")
            
            st.success("Interactive dashboard generated!")
            
            # Provide download button
            with open("outputs/interactive_dashboard.html", "rb") as f:
                st.download_button(
                    "Download Interactive Dashboard", 
                    f, 
                    "interactive_dashboard.html", 
                    mime="text/html",
                    help="Perfect for sharing on LinkedIn!"
                )
