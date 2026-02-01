# validators.py
# Core validation logic for data quality checks

import pandas as pd
import numpy as np
import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path


@dataclass
class Issue:
    """Represents a single data quality issue"""
    check_type: str          # e.g., 'missing_values', 'duplicates', 'date_format'
    severity: str            # 'LOW', 'MEDIUM', 'HIGH'
    message: str             # Human-readable description
    column: Optional[str] = None      # Which column has the issue
    row_count: Optional[int] = None   # How many rows affected
    details: Optional[Dict[str, Any]] = None  # Extra info


class DataValidator:
    """Core validation engine for data quality checks"""
    
    def __init__(self, df: pd.DataFrame, config_path: str = "config/rules.json"):
        """
        Initialize validator with a dataframe and configuration
        
        Args:
            df: The pandas DataFrame to validate
            config_path: Path to JSON config file with validation rules
        """
        self.df = df
        self.issues = []
        
        # Load configuration
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {config_path}. Using defaults.")
            self.config = self._default_config()
    
    def _default_config(self) -> dict:
        """Return default configuration if config file is missing"""
        return {
            "thresholds": {
                "missing_percent_high": 30,
                "missing_percent_medium": 10,
                "outlier_std_dev": 3
            },
            "critical_columns": [],
            "required_columns": []
        }
    
    def run_all_validations(self) -> List[Issue]:
        """
        Run all validation checks and return list of issues found
        
        Returns:
            List of Issue objects
        """
        print("Running all validations...")
        
        # Run each validation check
        self.check_missing_values_column()
        self.check_missing_values_row()
        self.check_duplicates()
        self.check_data_types()
        self.check_date_formats()
        self.check_outliers()
        self.check_required_columns()
        
        print(f"Validation complete. Found {len(self.issues)} issues.")
        return self.issues
    
    def check_missing_values_column(self):
        """Check for missing values in each column"""
        thresholds = self.config.get('thresholds', {})
        high_threshold = thresholds.get('missing_percent_high', 30)
        medium_threshold = thresholds.get('missing_percent_medium', 10)
        
        for column in self.df.columns:
            missing_count = self.df[column].isna().sum()
            if missing_count > 0:
                missing_percent = (missing_count / len(self.df)) * 100
                
                # Determine severity
                if missing_percent >= high_threshold:
                    severity = 'HIGH'
                elif missing_percent >= medium_threshold:
                    severity = 'MEDIUM'
                else:
                    severity = 'LOW'
                
                issue = Issue(
                    check_type='missing_values_column',
                    severity=severity,
                    message=f"Column '{column}' has {missing_count} missing values ({missing_percent:.1f}%)",
                    column=column,
                    row_count=missing_count,
                    details={'missing_percent': missing_percent}
                )
                self.issues.append(issue)
    
    def check_missing_values_row(self):
        """Check for rows with too many missing values"""
        # Find rows where more than 50% of values are missing
        row_missing_counts = self.df.isna().sum(axis=1)
        threshold = len(self.df.columns) * 0.5
        
        problematic_rows = row_missing_counts[row_missing_counts > threshold]
        
        if len(problematic_rows) > 0:
            issue = Issue(
                check_type='missing_values_row',
                severity='MEDIUM',
                message=f"Found {len(problematic_rows)} rows with more than 50% missing values",
                row_count=len(problematic_rows),
                details={'row_indices': problematic_rows.index.tolist()}
            )
            self.issues.append(issue)
    
    def check_duplicates(self, key_columns: Optional[List[str]] = None):
        """
        Check for duplicate rows
        
        Args:
            key_columns: Specific columns to check for duplicates. If None, checks all columns.
        """
        if key_columns:
            # Check duplicates based on specific columns
            duplicate_mask = self.df.duplicated(subset=key_columns, keep=False)
            duplicate_count = duplicate_mask.sum()
            
            if duplicate_count > 0:
                issue = Issue(
                    check_type='duplicates',
                    severity='HIGH',
                    message=f"Found {duplicate_count} duplicate rows based on key columns: {', '.join(key_columns)}",
                    row_count=duplicate_count,
                    details={'key_columns': key_columns}
                )
                self.issues.append(issue)
        else:
            # Check duplicates across all columns
            duplicate_count = self.df.duplicated().sum()
            
            if duplicate_count > 0:
                issue = Issue(
                    check_type='duplicates',
                    severity='MEDIUM',
                    message=f"Found {duplicate_count} fully duplicate rows",
                    row_count=duplicate_count
                )
                self.issues.append(issue)
    
    def check_data_types(self, expected_schema: Optional[Dict[str, str]] = None):
        """
        Check if columns have expected data types
        
        Args:
            expected_schema: Dictionary mapping column names to expected types
                            e.g., {'age': 'int64', 'name': 'object'}
        """
        if not expected_schema:
            # Just report current data types for info
            for column in self.df.columns:
                dtype = str(self.df[column].dtype)
                if dtype == 'object':
                    # Check if it could be converted to numeric or datetime
                    try:
                        pd.to_numeric(self.df[column], errors='raise')
                        issue = Issue(
                            check_type='data_type_suggestion',
                            severity='LOW',
                            message=f"Column '{column}' is stored as text but could be numeric",
                            column=column
                        )
                        self.issues.append(issue)
                    except:
                        pass
        else:
            # Check against expected schema
            for column, expected_type in expected_schema.items():
                if column in self.df.columns:
                    actual_type = str(self.df[column].dtype)
                    if actual_type != expected_type:
                        issue = Issue(
                            check_type='data_type_mismatch',
                            severity='MEDIUM',
                            message=f"Column '{column}' has type '{actual_type}' but expected '{expected_type}'",
                            column=column,
                            details={'expected': expected_type, 'actual': actual_type}
                        )
                        self.issues.append(issue)
    
    def check_date_formats(self, date_columns: Optional[List[str]] = None):
        """
        Check if date columns have valid date formats
        
        Args:
            date_columns: List of column names that should contain dates
        """
        if not date_columns:
            # Auto-detect potential date columns
            date_columns = []
            for column in self.df.columns:
                if 'date' in column.lower() or 'time' in column.lower():
                    date_columns.append(column)
        
        for column in date_columns:
            if column not in self.df.columns:
                continue
            
            try:
                # Try to convert to datetime
                pd.to_datetime(self.df[column], errors='raise')
            except Exception as e:
                # Count how many values can't be parsed
                parsed = pd.to_datetime(self.df[column], errors='coerce')
                invalid_count = parsed.isna().sum() - self.df[column].isna().sum()
                
                if invalid_count > 0:
                    issue = Issue(
                        check_type='invalid_date_format',
                        severity='MEDIUM',
                        message=f"Column '{column}' has {invalid_count} values that can't be parsed as dates",
                        column=column,
                        row_count=invalid_count
                    )
                    self.issues.append(issue)
    
    def check_outliers(self):
        """Check for statistical outliers in numeric columns"""
        thresholds = self.config.get('thresholds', {})
        std_dev_threshold = thresholds.get('outlier_std_dev', 3)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_cols:
            mean = self.df[column].mean()
            std = self.df[column].std()
            
            if std == 0:
                continue  # Skip if no variation
            
            # Find values beyond threshold standard deviations
            outliers = self.df[
                (self.df[column] < mean - std_dev_threshold * std) |
                (self.df[column] > mean + std_dev_threshold * std)
            ]
            
            if len(outliers) > 0:
                outlier_percent = (len(outliers) / len(self.df)) * 100
                
                issue = Issue(
                    check_type='outliers',
                    severity='LOW' if outlier_percent < 5 else 'MEDIUM',
                    message=f"Column '{column}' has {len(outliers)} outliers ({outlier_percent:.1f}%) beyond {std_dev_threshold} std devs",
                    column=column,
                    row_count=len(outliers),
                    details={'outlier_percent': outlier_percent}
                )
                self.issues.append(issue)
    
    def check_required_columns(self):
        """Check if all required columns are present"""
        required_columns = self.config.get('required_columns', [])
        
        for column in required_columns:
            if column not in self.df.columns:
                issue = Issue(
                    check_type='missing_required_column',
                    severity='HIGH',
                    message=f"Required column '{column}' is missing from dataset",
                    column=column
                )
                self.issues.append(issue)
    
    def check_value_ranges(self, range_rules: Optional[Dict[str, Dict[str, float]]] = None):
        """
        Check if values fall within expected ranges
        
        Args:
            range_rules: Dictionary like {'age': {'min': 0, 'max': 120}}
        """
        if not range_rules:
            return
        
        for column, rules in range_rules.items():
            if column not in self.df.columns:
                continue
            
            min_val = rules.get('min')
            max_val = rules.get('max')
            
            out_of_range = pd.Series([False] * len(self.df))
            
            if min_val is not None:
                out_of_range |= self.df[column] < min_val
            
            if max_val is not None:
                out_of_range |= self.df[column] > max_val
            
            count = out_of_range.sum()
            
            if count > 0:
                issue = Issue(
                    check_type='value_out_of_range',
                    severity='MEDIUM',
                    message=f"Column '{column}' has {count} values outside expected range [{min_val}, {max_val}]",
                    column=column,
                    row_count=count,
                    details={'min': min_val, 'max': max_val}
                )
                self.issues.append(issue)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all validation issues"""
        summary = {
            'total_issues': len(self.issues),
            'by_severity': {
                'HIGH': len([i for i in self.issues if i.severity == 'HIGH']),
                'MEDIUM': len([i for i in self.issues if i.severity == 'MEDIUM']),
                'LOW': len([i for i in self.issues if i.severity == 'LOW'])
            },
            'by_type': {}
        }
        
        for issue in self.issues:
            if issue.check_type not in summary['by_type']:
                summary['by_type'][issue.check_type] = 0
            summary['by_type'][issue.check_type] += 1
        
        return summary


# Example usage
if __name__ == "__main__":
    # Create sample data for testing
    sample_data = {
        'id': [1, 2, 3, 4, 5, 2],
        'name': ['Alice', 'Bob', None, 'David', 'Eve', 'Bob'],
        'age': [25, 30, 28, 150, 35, 30],
        'date_joined': ['2024-01-01', '2024-02-15', 'invalid', '2024-03-20', '2024-04-10', '2024-02-15']
    }
    df = pd.DataFrame(sample_data)
    
    # Run validation
    validator = DataValidator(df)
    issues = validator.run_all_validations()
    
    # Print issues
    print("\n=== VALIDATION ISSUES ===")
    for issue in issues:
        print(f"[{issue.severity}] {issue.message}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    summary = validator.get_summary()
    print(f"Total Issues: {summary['total_issues']}")
    print(f"High: {summary['by_severity']['HIGH']}, Medium: {summary['by_severity']['MEDIUM']}, Low: {summary['by_severity']['LOW']}")