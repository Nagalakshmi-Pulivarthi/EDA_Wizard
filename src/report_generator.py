# report_generator.py
# Generate validation reports and risk summaries

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from .validators import Issue
from .risk_engine import RiskScore

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class ReportGenerator:
    """
    Generates various reports from validation results
    Simple and human-readable output formats
    """
    
    def __init__(self, df: pd.DataFrame, issues: List[Issue], risk_score: Optional[RiskScore] = None):
        """
        Initialize report generator
        
        Args:
            df: The DataFrame that was validated
            issues: List of validation issues found
            risk_score: Optional RiskScore object
        """
        self.df = df
        self.issues = issues
        self.risk_score = risk_score
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_csv_report(self, output_path: str = "outputs/validation_report.csv"):
        """
        Generate a CSV report of all issues
        
        Args:
            output_path: Where to save the CSV file
        """
        if not self.issues:
            print("No issues to report!")
            return
        
        # Convert issues to DataFrame
        report_data = []
        for issue in self.issues:
            row = {
                'Severity': issue.severity,
                'Check Type': issue.check_type,
                'Message': issue.message,
                'Column': issue.column if issue.column else 'N/A',
                'Affected Rows': issue.row_count if issue.row_count else 'N/A',
                'Details': str(issue.details) if issue.details else 'N/A'
            }
            report_data.append(row)
        
        report_df = pd.DataFrame(report_data)
        
        # Sort by severity (HIGH first)
        severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        report_df['_sort'] = report_df['Severity'].map(severity_order)
        report_df = report_df.sort_values('_sort').drop('_sort', axis=1)
        
        # Save to CSV
        report_df.to_csv(output_path, index=False)
        print(f"✅ CSV report saved to {output_path}")
    
    def generate_excel_report(self, output_path: str = "outputs/validation_report.xlsx"):
        """
        Generate a comprehensive Excel report with multiple sheets
        
        Args:
            output_path: Where to save the Excel file
        """
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                # Sheet 1: Summary
                summary_data = {
                    'Metric': [
                        'Report Generated',
                        'Dataset Rows',
                        'Dataset Columns',
                        'Total Issues Found',
                        'High Severity Issues',
                        'Medium Severity Issues',
                        'Low Severity Issues'
                    ],
                    'Value': [
                        self.timestamp,
                        len(self.df),
                        len(self.df.columns),
                        len(self.issues),
                        len([i for i in self.issues if i.severity == 'HIGH']),
                        len([i for i in self.issues if i.severity == 'MEDIUM']),
                        len([i for i in self.issues if i.severity == 'LOW'])
                    ]
                }
                
                if self.risk_score:
                    summary_data['Metric'].extend([
                        'Risk Score',
                        'Risk Level'
                    ])
                    summary_data['Value'].extend([
                        f"{self.risk_score.total_score}/100",
                        self.risk_score.risk_level
                    ])
                
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Sheet 2: All Issues
                if self.issues:
                    issues_data = []
                    for issue in self.issues:
                        issues_data.append({
                            'Severity': issue.severity,
                            'Type': issue.check_type,
                            'Message': issue.message,
                            'Column': issue.column or 'N/A',
                            'Affected Rows': issue.row_count or 'N/A'
                        })
                    
                    issues_df = pd.DataFrame(issues_data)
                    severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
                    issues_df['_sort'] = issues_df['Severity'].map(severity_order)
                    issues_df = issues_df.sort_values('_sort').drop('_sort', axis=1)
                    issues_df.to_excel(writer, sheet_name='Issues', index=False)
                
                # Sheet 3: Data Overview
                overview_data = {
                    'Column': list(self.df.columns),
                    'Data Type': [str(dtype) for dtype in self.df.dtypes],
                    'Missing Count': [self.df[col].isna().sum() for col in self.df.columns],
                    'Missing %': [round((self.df[col].isna().sum() / len(self.df)) * 100, 2) for col in self.df.columns],
                    'Unique Values': [self.df[col].nunique() for col in self.df.columns]
                }
                pd.DataFrame(overview_data).to_excel(writer, sheet_name='Data Overview', index=False)
                
                # Sheet 4: Recommendations (if risk score available)
                if self.risk_score and self.risk_score.recommendations:
                    rec_data = {
                        'Priority': range(1, len(self.risk_score.recommendations) + 1),
                        'Recommendation': self.risk_score.recommendations
                    }
                    pd.DataFrame(rec_data).to_excel(writer, sheet_name='Recommendations', index=False)
        
            print(f"Excel report saved to {output_path}")
        except ImportError:
            print(f"Warning: openpyxl not installed. Skipping Excel report.")
            print(f"         Install with: pip install openpyxl")
        except Exception as e:
            print(f"Warning: Could not generate Excel report: {e}")
    
    def generate_html_report(self, output_path: str = "outputs/validation_report.html"):
        """
        Generate a nice HTML report with styling
        
        Args:
            output_path: Where to save the HTML file
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Validation Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .summary {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px 10px 0;
            padding: 10px 20px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
            text-transform: uppercase;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .risk-critical {{ color: #e74c3c; }}
        .risk-high {{ color: #e67e22; }}
        .risk-medium {{ color: #f39c12; }}
        .risk-low {{ color: #27ae60; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .severity-HIGH {{
            background-color: #ffe5e5;
            font-weight: bold;
        }}
        .severity-MEDIUM {{
            background-color: #fff5e5;
        }}
        .severity-LOW {{
            background-color: #e5f5ff;
        }}
        .recommendation {{
            background-color: #e8f5e9;
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #4caf50;
            border-radius: 3px;
        }}
        .timestamp {{
            color: #95a5a6;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Data Validation Report</h1>
        <p class="timestamp">Generated: {self.timestamp}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="metric">
                <div class="metric-label">Dataset Rows</div>
                <div class="metric-value">{len(self.df):,}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Columns</div>
                <div class="metric-value">{len(self.df.columns)}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Issues Found</div>
                <div class="metric-value">{len(self.issues)}</div>
            </div>
"""
        
        if self.risk_score:
            risk_class = f"risk-{self.risk_score.risk_level.lower()}"
            html += f"""
            <div class="metric">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value {risk_class}">{self.risk_score.risk_level}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Risk Score</div>
                <div class="metric-value">{self.risk_score.total_score}/100</div>
            </div>
"""
        
        html += """
        </div>
"""
        
        # Issues table
        if self.issues:
            html += """
        <h2>Issues Detected</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Type</th>
                <th>Message</th>
                <th>Column</th>
                <th>Affected Rows</th>
            </tr>
"""
            for issue in sorted(self.issues, key=lambda x: ['HIGH', 'MEDIUM', 'LOW'].index(x.severity)):
                html += f"""
            <tr class="severity-{issue.severity}">
                <td><strong>{issue.severity}</strong></td>
                <td>{issue.check_type}</td>
                <td>{issue.message}</td>
                <td>{issue.column or 'N/A'}</td>
                <td>{issue.row_count or 'N/A'}</td>
            </tr>
"""
            html += """
        </table>
"""
        
        # Recommendations
        if self.risk_score and self.risk_score.recommendations:
            html += """
        <h2>Recommendations</h2>
"""
            for rec in self.risk_score.recommendations:
                html += f'        <div class="recommendation">{rec}</div>\n'
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML report saved to {output_path}")
    
    def generate_plotly_dashboard(self, output_path: str = "outputs/interactive_dashboard.html"):
        """
        Generate an interactive Plotly dashboard
        Perfect for sharing on LinkedIn and GitHub!
        
        Args:
            output_path: Where to save the HTML file
        """
        if not PLOTLY_AVAILABLE:
            print("⚠️  Plotly not installed. Skipping interactive dashboard.")
            print("   Install with: pip install plotly")
            return
        
        # Create subplots layout
        fig = make_subplots(
            rows=3, cols=2,
            row_heights=[0.25, 0.35, 0.4],
            column_widths=[0.5, 0.5],
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}],
                [{"type": "bar", "colspan": 2}, None],
                [{"type": "table", "colspan": 2}, None]
            ],
            subplot_titles=(
                "Total Issues", "Risk Score",
                "Issues by Severity & Type",
                "Detailed Issues"
            ),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # KPI 1: Total Issues
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=len(self.issues),
                title={"text": "Total Issues Found"},
                delta={'reference': 0, 'increasing': {'color': "red"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=1
        )
        
        # KPI 2: Risk Score
        risk_score_value = self.risk_score.total_score if self.risk_score else 0
        risk_color = "red" if risk_score_value > 70 else "orange" if risk_score_value > 40 else "green"
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=risk_score_value,
                title={"text": "Risk Score"},
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
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=2
        )
        
        # Chart: Issues by Severity and Type
        if self.issues:
            # Count by severity
            severity_counts = {}
            type_counts = {}
            for issue in self.issues:
                severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
                type_counts[issue.check_type] = type_counts.get(issue.check_type, 0) + 1
            
            # Severity bar chart
            severity_order = ['HIGH', 'MEDIUM', 'LOW']
            severity_colors = {'HIGH': '#e74c3c', 'MEDIUM': '#f39c12', 'LOW': '#3498db'}
            
            severities = [s for s in severity_order if s in severity_counts]
            counts = [severity_counts[s] for s in severities]
            colors = [severity_colors[s] for s in severities]
            
            fig.add_trace(
                go.Bar(
                    x=severities,
                    y=counts,
                    name="By Severity",
                    marker_color=colors,
                    text=counts,
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Update bar chart layout
            fig.update_xaxes(title_text="Severity Level", row=2, col=1)
            fig.update_yaxes(title_text="Number of Issues", row=2, col=1)
        
        # Table: Detailed Issues
        if self.issues:
            # Sort issues by severity
            sorted_issues = sorted(self.issues, key=lambda x: ['HIGH', 'MEDIUM', 'LOW'].index(x.severity))
            
            table_data = {
                'Severity': [issue.severity for issue in sorted_issues],
                'Type': [issue.check_type for issue in sorted_issues],
                'Message': [issue.message[:80] + '...' if len(issue.message) > 80 else issue.message 
                           for issue in sorted_issues],
                'Column': [issue.column or 'N/A' for issue in sorted_issues],
                'Rows': [issue.row_count or 'N/A' for issue in sorted_issues]
            }
            
            # Color code severity
            severity_colors_table = {
                'HIGH': '#ffcccc',
                'MEDIUM': '#fff4cc',
                'LOW': '#cce5ff'
            }
            cell_colors = [[severity_colors_table.get(sev, 'white')] * 5 for sev in table_data['Severity']]
            cell_colors_transposed = list(map(list, zip(*cell_colors)))
            
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=['<b>Severity</b>', '<b>Type</b>', '<b>Message</b>', '<b>Column</b>', '<b>Affected Rows</b>'],
                        fill_color='#34495e',
                        font=dict(color='white', size=12),
                        align='left'
                    ),
                    cells=dict(
                        values=[table_data['Severity'], table_data['Type'], table_data['Message'], 
                               table_data['Column'], table_data['Rows']],
                        fill_color=cell_colors_transposed,
                        align='left',
                        height=25
                    )
                ),
                row=3, col=1
            )
        
        # Update overall layout
        fig.update_layout(
            title={
                'text': f"<b>Data Quality Control Dashboard</b><br><sub>Generated: {self.timestamp}</sub>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            showlegend=False,
            height=1000,
            font=dict(family="Arial, sans-serif", size=12),
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            margin=dict(t=100, l=50, r=50, b=50)
        )
        
        # Save to HTML
        fig.write_html(
            output_path,
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
            }
        )
        
        print(f"✅ Interactive Plotly dashboard saved to {output_path}")
        print(f"   📊 Open in browser to explore!")
    
    def print_console_summary(self):
        """Print a nice summary to console"""
        print("\n" + "="*60)
        print("           DATA VALIDATION SUMMARY")
        print("="*60)
        print(f"Timestamp: {self.timestamp}")
        print(f"Dataset: {len(self.df)} rows × {len(self.df.columns)} columns")
        print(f"\nIssues Found: {len(self.issues)}")
        print(f"  ├─ HIGH:   {len([i for i in self.issues if i.severity == 'HIGH'])}")
        print(f"  ├─ MEDIUM: {len([i for i in self.issues if i.severity == 'MEDIUM'])}")
        print(f"  └─ LOW:    {len([i for i in self.issues if i.severity == 'LOW'])}")
        
        if self.risk_score:
            print(f"\nRisk Assessment:")
            print(f"  Risk Level: {self.risk_score.risk_level}")
            print(f"  Risk Score: {self.risk_score.total_score}/100")
        
        print("="*60 + "\n")
    
    def generate_all_reports(self, output_dir: str = "outputs"):
        """
        Generate all report types at once
        
        Args:
            output_dir: Directory to save all reports
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print("\n📝 Generating reports...")
        
        self.generate_csv_report(f"{output_dir}/validation_report.csv")
        self.generate_excel_report(f"{output_dir}/validation_report.xlsx")
        self.generate_html_report(f"{output_dir}/validation_report.html")
        self.generate_plotly_dashboard(f"{output_dir}/interactive_dashboard.html")
        self.print_console_summary()
        
        print("✅ All reports generated successfully!")


# Example usage
if __name__ == "__main__":
    from validators import DataValidator
    from risk_engine import RiskEngine
    
    # Create sample data
    sample_data = {
        'id': [1, 2, 3, 4, 5, 2],
        'name': ['Alice', 'Bob', None, 'David', 'Eve', 'Bob'],
        'age': [25, 30, 28, 150, 35, 30]
    }
    df = pd.DataFrame(sample_data)
    
    # Run validation
    validator = DataValidator(df)
    issues = validator.run_all_validations()
    
    # Calculate risk
    risk_engine = RiskEngine()
    risk_score = risk_engine.calculate_risk(issues, df)
    
    # Generate reports
    reporter = ReportGenerator(df, issues, risk_score)
    reporter.generate_all_reports()
