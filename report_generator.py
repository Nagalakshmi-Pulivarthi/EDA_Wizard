# report_generator.py
# Generate reports in different formats

import pandas as pd
from datetime import datetime
from pathlib import Path

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class ReportGenerator:
    """Generates reports from validation results"""
    
    def __init__(self, df, issues, risk_score=None):
        self.df = df
        self.issues = issues
        self.risk_score = risk_score
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_html_report(self, output_path="outputs/validation_report.html"):
        """Generate a nice HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Validation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
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
        }}
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
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
        .severity-HIGH {{ background-color: #ffe5e5; }}
        .severity-MEDIUM {{ background-color: #fff5e5; }}
        .severity-LOW {{ background-color: #e5f5ff; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Data Validation Report</h1>
        <p>Generated: {self.timestamp}</p>
        
        <div class="summary">
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
            html += f"""
            <div class="metric">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value">{self.risk_score.risk_level}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Risk Score</div>
                <div class="metric-value">{self.risk_score.total_score}/100</div>
            </div>
"""
        
        html += """
        </div>
"""
        
        if self.issues:
            html += """
        <h2>Issues Detected</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Type</th>
                <th>Message</th>
                <th>Column</th>
            </tr>
"""
            for issue in sorted(self.issues, key=lambda x: ['HIGH', 'MEDIUM', 'LOW'].index(x.severity)):
                html += f"""
            <tr class="severity-{issue.severity}">
                <td><strong>{issue.severity}</strong></td>
                <td>{issue.check_type}</td>
                <td>{issue.message}</td>
                <td>{issue.column or 'N/A'}</td>
            </tr>
"""
            html += """
        </table>
"""
        
        if self.risk_score and self.risk_score.recommendations:
            html += """
        <h2>Recommendations</h2>
"""
            for rec in self.risk_score.recommendations:
                html += f'        <div style="margin: 10px 0; padding: 10px; background: #e8f5e9; border-left: 4px solid #4caf50;">{rec}</div>\n'
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML report saved to {output_path}")
    
    def generate_plotly_dashboard(self, output_path="outputs/interactive_dashboard.html"):
        """Generate an interactive dashboard (if Plotly is installed)"""
        if not PLOTLY_AVAILABLE:
            print("⚠️  Plotly not installed. Skipping interactive dashboard.")
            return
        
        # Create a simple dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Total Issues", "Risk Score", "Issues by Severity", ""),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "bar", "colspan": 2}, None]]
        )
        
        # Total issues indicator
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=len(self.issues),
                title={"text": "Total Issues"}
            ),
            row=1, col=1
        )
        
        # Risk score gauge
        risk_score_value = self.risk_score.total_score if self.risk_score else 0
        risk_color = "red" if risk_score_value > 70 else "orange" if risk_score_value > 40 else "green"
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=risk_score_value,
                title={"text": "Risk Score"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': risk_color}}
            ),
            row=1, col=2
        )
        
        # Issues by severity
        if self.issues:
            severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
            for issue in self.issues:
                severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
            
            colors = {'HIGH': '#e74c3c', 'MEDIUM': '#f39c12', 'LOW': '#3498db'}
            
            fig.add_trace(
                go.Bar(
                    x=list(severity_counts.keys()),
                    y=list(severity_counts.values()),
                    marker_color=[colors[k] for k in severity_counts.keys()],
                    text=list(severity_counts.values()),
                    textposition='auto'
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title=f"<b>Data Quality Dashboard</b><br><sub>{self.timestamp}</sub>",
            showlegend=False,
            height=800
        )
        
        fig.write_html(output_path)
        print(f"✅ Interactive dashboard saved to {output_path}")
    
    def generate_all_reports(self, output_dir="outputs"):
        """Generate all reports"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print("\n📝 Generating reports...")
        self.generate_html_report(f"{output_dir}/validation_report.html")
        self.generate_plotly_dashboard(f"{output_dir}/interactive_dashboard.html")
        print("✅ All reports generated!")
