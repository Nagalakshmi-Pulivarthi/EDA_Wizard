# risk_engine.py
# This calculates how risky it is to use the data based on the issues found
# Gives a score from 0-100 where higher = worse

import pandas as pd
import json
from .validators import Issue


class RiskScore:
    """
    Stores the overall risk assessment for a dataset
    Includes the score, risk level, and recommendations
    """
    def __init__(self, total_score, risk_level, issue_count, high_severity_count, recommendations):
        self.total_score = total_score              # The risk score (0-100, higher is worse)
        self.risk_level = risk_level                # LOW, MEDIUM, HIGH, or CRITICAL
        self.issue_count = issue_count              # How many issues were found total
        self.high_severity_count = high_severity_count  # How many HIGH severity issues
        self.recommendations = recommendations      # List of what to fix


class RiskEngine:
    """
    This class calculates how risky your data is based on the issues found
    Different types of issues get different point values
    """
    
    def __init__(self, config_path="config/rules.json"):
        self.config_path = config_path
        # Load the weights that determine how serious each issue type is
        self.risk_weights = self._load_risk_weights()
    
    def _load_risk_weights(self):
        """
        Try to load risk weights from config file
        If the file doesn't exist, use the defaults
        """
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get('risk_weights', self._default_weights())
        except FileNotFoundError:
            print(f"Couldn't find config file, using default weights")
            return self._default_weights()
    
    def _default_weights(self):
        """
        These are the default point values for each issue type
        Higher points = more serious problem
        Missing required columns is the worst (10 points)
        """
        return {
            'missing_values_column': {'points': 2, 'multiplier': 1.0},
            'missing_values_row': {'points': 3, 'multiplier': 1.0},
            'duplicates': {'points': 5, 'multiplier': 1.0},
            'invalid_date_format': {'points': 2, 'multiplier': 1.0},
            'data_type_mismatch': {'points': 3, 'multiplier': 1.0},
            'outliers': {'points': 1, 'multiplier': 1.0},
            'missing_required_column': {'points': 10, 'multiplier': 1.0},  # Worst!
            'value_out_of_range': {'points': 3, 'multiplier': 1.0}
        }
    
    def calculate_risk(self, issues, df):
        """
        This is the main function that calculates the risk score
        It adds up points from each issue and converts it to a 0-100 scale
        """
        print("Calculating risk score...")
        
        total_points = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        
        # Go through each issue and count by severity
        for issue in issues:
            if issue.severity == 'HIGH':
                high_count += 1
            elif issue.severity == 'MEDIUM':
                medium_count += 1
            elif issue.severity == 'LOW':
                low_count += 1
            
            # Get the base points for this type of issue
            # If we don't have a weight for it, default to 1 point
            issue_weight = self.risk_weights.get(
                issue.check_type,
                {'points': 1, 'multiplier': 1.0}
            )
            
            base_points = issue_weight.get('points', 1)
            multiplier = issue_weight.get('multiplier', 1.0)
            
            # HIGH severity issues are doubled
            # MEDIUM issues are multiplied by 1.5
            if issue.severity == 'HIGH':
                base_points *= 2
            elif issue.severity == 'MEDIUM':
                base_points *= 1.5
            
            # If more than 50% of data is affected, make it even worse
            if issue.details and 'missing_percent' in issue.details:
                percent = issue.details['missing_percent']
                if percent > 50:
                    multiplier *= 1.5  # Extra penalty for affecting lots of data
            
            total_points += base_points * multiplier
        
        # Convert points to a 0-100 scale
        # I chose 50 points as the baseline for 100% risk
        risk_score = min(100, (total_points / 50) * 100)
        
        # Decide the risk level based on score and number of HIGH issues
        if risk_score >= 75 or high_count >= 5:
            risk_level = 'CRITICAL'  # Really bad - don't use this data!
        elif risk_score >= 50 or high_count >= 3:
            risk_level = 'HIGH'       # Serious problems
        elif risk_score >= 25 or medium_count >= 5:
            risk_level = 'MEDIUM'     # Some issues to fix
        else:
            risk_level = 'LOW'        # Minor issues, data is usable
        
        # Generate helpful recommendations based on what we found
        recommendations = self._generate_recommendations(issues, df, risk_level)
        
        # Create and return the RiskScore object
        return RiskScore(
            total_score=round(risk_score, 2),
            risk_level=risk_level,
            issue_count=len(issues),
            high_severity_count=high_count,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, issues, df, risk_level):
        """
        Generate recommendations on what to fix based on the issues
        Helps users know where to start
        """
        recommendations = []
        
        # First, handle HIGH severity issues - these are urgent
        high_issues = [i for i in issues if i.severity == 'HIGH']
        if high_issues:
            recommendations.append("🔴 URGENT: Fix these HIGH severity issues first")
            
            # Give specific advice for the top 3 high issues
            for issue in high_issues[:3]:
                if issue.check_type == 'missing_required_column':
                    recommendations.append(f"   → Missing column: {issue.column}")
                elif issue.check_type == 'duplicates':
                    recommendations.append(f"   → Remove {issue.row_count} duplicate rows")
                elif issue.check_type == 'missing_values_column':
                    recommendations.append(f"   → Fix missing data in '{issue.column}'")
        
        # Check for missing data issues
        missing_issues = [i for i in issues if 'missing' in i.check_type]
        if missing_issues:
            recommendations.append("📊 Consider filling in missing values (imputation) or removing those rows")
        
        # Check for duplicates
        dup_issues = [i for i in issues if i.check_type == 'duplicates']
        if dup_issues:
            recommendations.append("🔍 Remove duplicate records - they can skew your analysis")
        
        # Check for data type problems
        type_issues = [i for i in issues if 'type' in i.check_type]
        if type_issues:
            recommendations.append("🔧 Convert columns to the right types (numbers should be numeric, not text)")
        
        # Check for date issues
        date_issues = [i for i in issues if 'date' in i.check_type]
        if date_issues:
            recommendations.append("📅 Fix date formats so they're all consistent")
        
        # Check for outliers
        outlier_issues = [i for i in issues if i.check_type == 'outliers']
        if outlier_issues:
            recommendations.append("📈 Check if outliers are errors or real unusual values")
        
        # Overall recommendation based on risk level
        if risk_level in ['HIGH', 'CRITICAL']:
            recommendations.append("⚠️ Don't use this data for important analysis until you fix these issues")
        elif risk_level == 'MEDIUM':
            recommendations.append("⚡ Fix the medium priority issues before analyzing")
        else:
            recommendations.append("✅ Data looks good enough to analyze")
        
        return recommendations
    
    def generate_summary_text(self, risk_score):
        """
        Create a nice formatted text summary of the risk assessment
        This gets printed to the console or saved to a text file
        """
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
        
        return summary
    
    def export_risk_summary(self, risk_score, issues, output_path="outputs/risk_summary.txt"):
        """
        Save the risk summary to a text file
        This creates a nice formatted report you can share or review later
        """
        # Generate the main summary text
        summary_text = self.generate_summary_text(risk_score)
        
        # Add a detailed breakdown of all issues
        summary_text += "\n\n" + "="*60 + "\n"
        summary_text += "DETAILED ISSUE BREAKDOWN\n"
        summary_text += "="*60 + "\n\n"
        
        # Sort issues so HIGH severity comes first (reverse=True does this)
        for issue in sorted(issues, key=lambda x: ['LOW', 'MEDIUM', 'HIGH'].index(x.severity), reverse=True):
            summary_text += f"[{issue.severity}] {issue.check_type}\n"
            summary_text += f"    {issue.message}\n\n"
        
        # Write everything to a file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        
        print(f"✅ Risk summary saved to {output_path}")
        
        return summary_text


# You can run this file directly to test the risk engine
if __name__ == "__main__":
    from validators import DataValidator
    
    # Create some sample data with problems
    sample_data = {
        'id': [1, 2, 3, 4, 5, 2],              # Has duplicate (id=2 twice)
        'name': ['Alice', 'Bob', None, 'David', 'Eve', 'Bob'],  # Missing value
        'age': [25, 30, 28, 150, 35, 30]       # 150 is an outlier
    }
    df = pd.DataFrame(sample_data)
    
    # Run validation to find issues
    validator = DataValidator(df)
    issues = validator.run_all_validations()
    
    # Calculate the risk score
    risk_engine = RiskEngine()
    risk_score = risk_engine.calculate_risk(issues, df)
    
    # Print the summary
    print(risk_engine.generate_summary_text(risk_score))
