# validators.py
# This is where all the data quality checks happen
# Checks for missing values, duplicates, outliers, etc.

import pandas as pd
import numpy as np


class Issue:
    """
    Simple class to store information about a data quality problem
    Makes it easier to keep track of what's wrong with the data
    """
    def __init__(self, check_type, severity, message, column=None, row_count=None, details=None):
        self.check_type = check_type    # What kind of problem (missing_values, duplicates, etc.)
        self.severity = severity          # How bad is it? LOW, MEDIUM, or HIGH
        self.message = message            # A clear message about the problem
        self.column = column              # Which column has the problem (if specific)
        self.row_count = row_count        # How many rows are affected
        self.details = details            # Any extra info we want to store


class DataValidator:
    """
    The main class that checks your data for problems
    Pass in a dataframe and it will run all the checks
    """
    
    def __init__(self, df):
        # Store the dataframe we're going to check
        self.df = df
        
        # This list will hold all the issues we find
        self.issues = []
        
        # Simple thresholds - adjust these if you want
        self.missing_percent_high = 30     # More than 30% missing = serious problem
        self.missing_percent_medium = 10   # 10-30% missing = warning
        self.outlier_std_dev = 3           # Values beyond 3 standard deviations = outlier
    
    def run_all_validations(self):
        """
        This is the main function - it runs all the checks on your data
        Returns a list of all issues it found
        """
        print("Starting data quality checks...")
        
        # Run each check one by one
        self.check_missing_values_column()
        self.check_missing_values_row()
        self.check_duplicates()
        self.check_data_types()
        self.check_date_formats()
        self.check_outliers()
        
        print(f"Done! Found {len(self.issues)} issues total.")
        return self.issues
    
    def check_missing_values_column(self):
        """Check each column for missing/null values"""
        for column in self.df.columns:
            missing_count = self.df[column].isna().sum()
            
            if missing_count > 0:
                missing_percent = (missing_count / len(self.df)) * 100
                
                # Decide how serious this is
                if missing_percent >= self.missing_percent_high:
                    severity = 'HIGH'
                elif missing_percent >= self.missing_percent_medium:
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
        """Check for rows that are mostly empty"""
        row_missing_counts = self.df.isna().sum(axis=1)
        threshold = len(self.df.columns) * 0.5
        problematic_rows = row_missing_counts[row_missing_counts > threshold]
        
        if len(problematic_rows) > 0:
            issue = Issue(
                check_type='missing_values_row',
                severity='MEDIUM',
                message=f"Found {len(problematic_rows)} rows that are more than half empty",
                row_count=len(problematic_rows)
            )
            self.issues.append(issue)
    
    def check_duplicates(self):
        """Look for duplicate rows in the data"""
        duplicate_count = self.df.duplicated().sum()
        
        if duplicate_count > 0:
            issue = Issue(
                check_type='duplicates',
                severity='MEDIUM',
                message=f"Found {duplicate_count} rows that are exact duplicates",
                row_count=duplicate_count
            )
            self.issues.append(issue)
    
    def check_data_types(self):
        """Check if columns have the right data types"""
        for column in self.df.columns:
            dtype = str(self.df[column].dtype)
            
            if dtype == 'object':
                # Check if text column could be numbers
                try:
                    pd.to_numeric(self.df[column], errors='raise')
                    issue = Issue(
                        check_type='data_type_suggestion',
                        severity='LOW',
                        message=f"Column '{column}' is stored as text but looks like it should be numbers",
                        column=column
                    )
                    self.issues.append(issue)
                except:
                    pass
    
    def check_date_formats(self):
        """Check if date columns are properly formatted"""
        date_columns = [col for col in self.df.columns 
                       if 'date' in col.lower() or 'time' in col.lower()]
        
        for column in date_columns:
            try:
                pd.to_datetime(self.df[column], errors='raise')
            except:
                parsed = pd.to_datetime(self.df[column], errors='coerce')
                invalid_count = parsed.isna().sum() - self.df[column].isna().sum()
                
                if invalid_count > 0:
                    issue = Issue(
                        check_type='invalid_date_format',
                        severity='MEDIUM',
                        message=f"Column '{column}' has {invalid_count} dates that couldn't be parsed",
                        column=column,
                        row_count=invalid_count
                    )
                    self.issues.append(issue)
    
    def check_outliers(self):
        """Find outliers in numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_cols:
            mean = self.df[column].mean()
            std = self.df[column].std()
            
            if std == 0:
                continue
            
            outliers = self.df[
                (self.df[column] < mean - self.outlier_std_dev * std) |
                (self.df[column] > mean + self.outlier_std_dev * std)
            ]
            
            if len(outliers) > 0:
                outlier_percent = (len(outliers) / len(self.df)) * 100
                
                issue = Issue(
                    check_type='outliers',
                    severity='LOW' if outlier_percent < 5 else 'MEDIUM',
                    message=f"Column '{column}' has {len(outliers)} outliers ({outlier_percent:.1f}%)",
                    column=column,
                    row_count=len(outliers)
                )
                self.issues.append(issue)
