# risk_calculator.py
# Calculates how risky it is to use the data
# Gives a score from 0-100 where higher = worse

import pandas as pd


class RiskScore:
    """Stores the overall risk assessment for a dataset"""
    def __init__(self, total_score, risk_level, issue_count, high_severity_count, recommendations):
        self.total_score = total_score
        self.risk_level = risk_level
        self.issue_count = issue_count
        self.high_severity_count = high_severity_count
        self.recommendations = recommendations


class RiskCalculator:
    """Calculates how risky your data is based on the issues found"""
    
    def __init__(self):
        # How many points each issue type is worth
        self.points = {
            'missing_values_column': 2,
            'missing_values_row': 3,
            'duplicates': 5,
            'invalid_date_format': 2,
            'data_type_mismatch': 3,
            'outliers': 1,
            'value_out_of_range': 3
        }
    
    def calculate_risk(self, issues, df):
        """Calculate the risk score from 0-100"""
        print("Calculating risk score...")
        
        total_points = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        
        # Count up the points
        for issue in issues:
            if issue.severity == 'HIGH':
                high_count += 1
            elif issue.severity == 'MEDIUM':
                medium_count += 1
            elif issue.severity == 'LOW':
                low_count += 1
            
            # Get base points for this issue type
            base_points = self.points.get(issue.check_type, 1)
            
            # Multiply based on severity
            if issue.severity == 'HIGH':
                base_points *= 2
            elif issue.severity == 'MEDIUM':
                base_points *= 1.5
            
            # Extra penalty if lots of data is affected
            if issue.details and 'missing_percent' in issue.details:
                if issue.details['missing_percent'] > 50:
                    base_points *= 1.5
            
            total_points += base_points
        
        # Convert to 0-100 scale
        risk_score = min(100, (total_points / 50) * 100)
        
        # Decide the risk level
        if risk_score >= 75 or high_count >= 5:
            risk_level = 'CRITICAL'
        elif risk_score >= 50 or high_count >= 3:
            risk_level = 'HIGH'
        elif risk_score >= 25 or medium_count >= 5:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # Generate recommendations
        recommendations = self._make_recommendations(issues, risk_level)
        
        return RiskScore(
            total_score=round(risk_score, 2),
            risk_level=risk_level,
            issue_count=len(issues),
            high_severity_count=high_count,
            recommendations=recommendations
        )
    
    def _make_recommendations(self, issues, risk_level):
        """Generate helpful recommendations"""
        recommendations = []
        
        # Check for high severity issues
        high_issues = [i for i in issues if i.severity == 'HIGH']
        if high_issues:
            recommendations.append("🔴 URGENT: Fix these HIGH severity issues first")
            for issue in high_issues[:3]:
                if issue.check_type == 'duplicates':
                    recommendations.append(f"   → Remove {issue.row_count} duplicate rows")
                elif issue.check_type == 'missing_values_column':
                    recommendations.append(f"   → Fix missing data in '{issue.column}'")
        
        # Check for missing data
        if any('missing' in i.check_type for i in issues):
            recommendations.append("📊 Fill in missing values or remove those rows")
        
        # Check for duplicates
        if any(i.check_type == 'duplicates' for i in issues):
            recommendations.append("🔍 Remove duplicate records")
        
        # Check for data types
        if any('type' in i.check_type for i in issues):
            recommendations.append("🔧 Convert columns to the right types")
        
        # Check for dates
        if any('date' in i.check_type for i in issues):
            recommendations.append("📅 Fix date formats")
        
        # Check for outliers
        if any(i.check_type == 'outliers' for i in issues):
            recommendations.append("📈 Check if outliers are errors or real values")
        
        # Overall recommendation
        if risk_level in ['HIGH', 'CRITICAL']:
            recommendations.append("⚠️ Don't use this data until you fix these issues")
        elif risk_level == 'MEDIUM':
            recommendations.append("⚡ Fix the medium priority issues before analyzing")
        else:
            recommendations.append("✅ Data looks good enough to analyze")
        
        return recommendations
    
    def export_risk_summary(self, risk_score, issues, output_path="outputs/risk_summary.txt"):
        """Save the risk summary to a text file"""
        summary = f"""
╔══════════════════════════════════════════════════════════╗
║           DATA QUALITY RISK ASSESSMENT                   ║
╚══════════════════════════════════════════════════════════╝

Risk Level: {risk_score.risk_level}
Risk Score: {risk_score.total_score}/100

Issues Found: {risk_score.issue_count} total
  └─ High Severity: {risk_score.high_severity_count}

RECOMMENDATIONS:
"""
        for i, rec in enumerate(risk_score.recommendations, 1):
            summary += f"{i}. {rec}\n"
        
        summary += "\n\n" + "="*60 + "\n"
        summary += "DETAILED ISSUE BREAKDOWN\n"
        summary += "="*60 + "\n\n"
        
        for issue in sorted(issues, key=lambda x: ['LOW', 'MEDIUM', 'HIGH'].index(x.severity), reverse=True):
            summary += f"[{issue.severity}] {issue.check_type}\n"
            summary += f"    {issue.message}\n\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ Risk summary saved to {output_path}")
