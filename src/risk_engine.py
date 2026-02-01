# risk_engine.py
# Risk scoring engine for quantifying data quality issues

import pandas as pd
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .validators import Issue


@dataclass
class RiskScore:
    """Represents a risk score for the dataset"""
    total_score: float           # Overall risk score (0-100)
    risk_level: str              # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    issue_count: int             # Total number of issues
    high_severity_count: int     # Count of high severity issues
    recommendations: List[str]   # List of recommendations


class RiskEngine:
    """
    Calculates risk scores based on data quality issues
    Simple scoring system that anyone can understand
    """
    
    def __init__(self, config_path: str = "config/rules.json"):
        """
        Initialize risk engine
        
        Args:
            config_path: Path to configuration file with risk weights
        """
        self.config_path = config_path
        self.risk_weights = self._load_risk_weights()
    
    def _load_risk_weights(self) -> Dict[str, Dict[str, Any]]:
        """Load risk weights from config file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get('risk_weights', self._default_weights())
        except FileNotFoundError:
            print(f"Config file not found. Using default risk weights.")
            return self._default_weights()
    
    def _default_weights(self) -> Dict[str, Dict[str, Any]]:
        """Default risk weight configuration"""
        return {
            'missing_values_column': {'points': 2, 'multiplier': 1.0},
            'missing_values_row': {'points': 3, 'multiplier': 1.0},
            'duplicates': {'points': 5, 'multiplier': 1.0},
            'invalid_date_format': {'points': 2, 'multiplier': 1.0},
            'data_type_mismatch': {'points': 3, 'multiplier': 1.0},
            'outliers': {'points': 1, 'multiplier': 1.0},
            'missing_required_column': {'points': 10, 'multiplier': 1.0},
            'value_out_of_range': {'points': 3, 'multiplier': 1.0}
        }
    
    def calculate_risk(self, issues: List[Issue], df: pd.DataFrame) -> RiskScore:
        """
        Calculate overall risk score based on issues found
        
        Args:
            issues: List of Issue objects from validation
            df: The DataFrame that was validated
            
        Returns:
            RiskScore object with overall assessment
        """
        print("Calculating risk score...")
        
        total_points = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        
        # Count issues by severity
        for issue in issues:
            if issue.severity == 'HIGH':
                high_count += 1
            elif issue.severity == 'MEDIUM':
                medium_count += 1
            elif issue.severity == 'LOW':
                low_count += 1
            
            # Add points based on issue type
            issue_weight = self.risk_weights.get(
                issue.check_type,
                {'points': 1, 'multiplier': 1.0}
            )
            
            base_points = issue_weight.get('points', 1)
            multiplier = issue_weight.get('multiplier', 1.0)
            
            # Adjust points by severity
            if issue.severity == 'HIGH':
                base_points *= 2
            elif issue.severity == 'MEDIUM':
                base_points *= 1.5
            
            # Adjust by percentage affected (if available)
            if issue.details and 'missing_percent' in issue.details:
                percent = issue.details['missing_percent']
                if percent > 50:
                    multiplier *= 1.5
            
            total_points += base_points * multiplier
        
        # Normalize to 0-100 scale
        # Assume 50 points = max risk for normalization
        risk_score = min(100, (total_points / 50) * 100)
        
        # Determine risk level
        if risk_score >= 75 or high_count >= 5:
            risk_level = 'CRITICAL'
        elif risk_score >= 50 or high_count >= 3:
            risk_level = 'HIGH'
        elif risk_score >= 25 or medium_count >= 5:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # Generate recommendations
        recommendations = self._generate_recommendations(issues, df, risk_level)
        
        return RiskScore(
            total_score=round(risk_score, 2),
            risk_level=risk_level,
            issue_count=len(issues),
            high_severity_count=high_count,
            recommendations=recommendations
        )
    
    def _generate_recommendations(
        self,
        issues: List[Issue],
        df: pd.DataFrame,
        risk_level: str
    ) -> List[str]:
        """Generate actionable recommendations based on issues found"""
        recommendations = []
        
        # High priority recommendations
        high_issues = [i for i in issues if i.severity == 'HIGH']
        if high_issues:
            recommendations.append("🔴 URGENT: Address all HIGH severity issues immediately")
            
            # Specific recommendations for high issues
            for issue in high_issues[:3]:  # Top 3 high issues
                if issue.check_type == 'missing_required_column':
                    recommendations.append(f"   → Add missing required column: {issue.column}")
                elif issue.check_type == 'duplicates':
                    recommendations.append(f"   → Remove {issue.row_count} duplicate records")
                elif issue.check_type == 'missing_values_column':
                    recommendations.append(f"   → Fix missing values in '{issue.column}' column")
        
        # Missing data recommendations
        missing_issues = [i for i in issues if 'missing' in i.check_type]
        if missing_issues:
            recommendations.append("📊 Consider data imputation strategies for missing values")
        
        # Duplicate recommendations
        dup_issues = [i for i in issues if i.check_type == 'duplicates']
        if dup_issues:
            recommendations.append("🔍 Review and remove duplicate records to ensure data integrity")
        
        # Data type recommendations
        type_issues = [i for i in issues if 'type' in i.check_type]
        if type_issues:
            recommendations.append("🔧 Convert columns to appropriate data types for better analysis")
        
        # Date format recommendations
        date_issues = [i for i in issues if 'date' in i.check_type]
        if date_issues:
            recommendations.append("📅 Standardize date formats across the dataset")
        
        # Outlier recommendations
        outlier_issues = [i for i in issues if i.check_type == 'outliers']
        if outlier_issues:
            recommendations.append("📈 Investigate outliers - they may be errors or important anomalies")
        
        # Overall data quality
        if risk_level in ['HIGH', 'CRITICAL']:
            recommendations.append("⚠️ Do NOT use this data for critical decisions until issues are resolved")
        elif risk_level == 'MEDIUM':
            recommendations.append("⚡ Address medium-priority issues before analysis")
        else:
            recommendations.append("✅ Data quality is acceptable for basic analysis")
        
        return recommendations
    
    def generate_summary_text(self, risk_score: RiskScore) -> str:
        """
        Generate a human-readable summary text
        
        Args:
            risk_score: RiskScore object
            
        Returns:
            Formatted string summary
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
    
    def export_risk_summary(
        self,
        risk_score: RiskScore,
        issues: List[Issue],
        output_path: str = "outputs/risk_summary.txt"
    ):
        """
        Export risk assessment to a text file
        
        Args:
            risk_score: RiskScore object
            issues: List of issues
            output_path: Where to save the summary
        """
        summary_text = self.generate_summary_text(risk_score)
        
        # Add detailed issue breakdown
        summary_text += "\n\n" + "="*60 + "\n"
        summary_text += "DETAILED ISSUE BREAKDOWN\n"
        summary_text += "="*60 + "\n\n"
        
        for issue in sorted(issues, key=lambda x: ['LOW', 'MEDIUM', 'HIGH'].index(x.severity), reverse=True):
            summary_text += f"[{issue.severity}] {issue.check_type}\n"
            summary_text += f"    {issue.message}\n\n"
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        
        print(f"✅ Risk summary saved to {output_path}")
        
        return summary_text


# Example usage
if __name__ == "__main__":
    from validators import DataValidator
    
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
    
    # Print summary
    print(risk_engine.generate_summary_text(risk_score))
