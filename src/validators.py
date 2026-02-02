# validators.py
# This is where all the data quality checks happen
# Checks for missing values, duplicates, outliers, etc.

import pandas as pd
import numpy as np
import json


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
    
    def __init__(self, df, config_path="config/rules.json"):
        # Store the dataframe we're going to check
        self.df = df
        
        # This list will hold all the issues we find
        self.issues = []
        
        # Try to load thresholds from config file
        # If the file doesn't exist, just use some reasonable defaults
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Couldn't find config file, using default thresholds instead")
            self.config = self._default_config()
    
    def _default_config(self):
        """
        These are the default thresholds I'm using
        You can adjust these based on what makes sense for your data
        """
        return {
            "thresholds": {
                "missing_percent_high": 30,     # More than 30% missing = serious problem
                "missing_percent_medium": 10,   # 10-30% missing = warning
                "outlier_std_dev": 3            # Values beyond 3 standard deviations = outlier
            },
            "critical_columns": [],
            "required_columns": []
        }
    
    def run_all_validations(self):
        """
        This is the main function - it runs all the checks on your data
        Returns a list of all issues it found
        """
        print("Starting data quality checks...")
        
        # Run each check one by one
        # Each of these functions adds issues to self.issues
        self.check_missing_values_column()
        self.check_missing_values_row()
        self.check_duplicates()
        self.check_data_types()
        self.check_date_formats()
        self.check_outliers()
        self.check_required_columns()
        
        print(f"Done! Found {len(self.issues)} issues total.")
        return self.issues
    
    def check_missing_values_column(self):
        """
        Check each column for missing/null values
        Missing data is one of the most common problems!
        """
        # Get our thresholds from the config
        thresholds = self.config.get('thresholds', {})
        high_threshold = thresholds.get('missing_percent_high', 30)
        medium_threshold = thresholds.get('missing_percent_medium', 10)
        
        # Go through each column in the dataframe
        for column in self.df.columns:
            # Count how many values are missing
            missing_count = self.df[column].isna().sum()
            
            if missing_count > 0:
                # Calculate what percentage of the column is missing
                missing_percent = (missing_count / len(self.df)) * 100
                
                # Decide how serious this is based on percentage
                if missing_percent >= high_threshold:
                    severity = 'HIGH'      # More than 30% missing = big problem
                elif missing_percent >= medium_threshold:
                    severity = 'MEDIUM'    # 10-30% = warning
                else:
                    severity = 'LOW'       # Less than 10% = minor issue
                
                # Create an Issue object to store this problem
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
        """
        Check for rows that are mostly empty
        If a row has more than half its values missing, that's usually a problem
        """
        # Count missing values in each row (axis=1 means count across columns)
        row_missing_counts = self.df.isna().sum(axis=1)
        
        # A row is "problematic" if more than 50% of its values are missing
        threshold = len(self.df.columns) * 0.5
        
        # Find the rows that exceed this threshold
        problematic_rows = row_missing_counts[row_missing_counts > threshold]
        
        if len(problematic_rows) > 0:
            # These rows are probably not very useful for analysis
            issue = Issue(
                check_type='missing_values_row',
                severity='MEDIUM',
                message=f"Found {len(problematic_rows)} rows that are more than half empty",
                row_count=len(problematic_rows),
                details={'row_indices': problematic_rows.index.tolist()}
            )
            self.issues.append(issue)
    
    def check_duplicates(self, key_columns=None):
        """
        Look for duplicate rows in the data
        Duplicates can mess up your analysis, so it's good to catch them
        """
        if key_columns:
            # If specific columns are provided, check for duplicates based on those
            duplicate_mask = self.df.duplicated(subset=key_columns, keep=False)
            duplicate_count = duplicate_mask.sum()
            
            if duplicate_count > 0:
                issue = Issue(
                    check_type='duplicates',
                    severity='HIGH',
                    message=f"Found {duplicate_count} duplicate rows (checking columns: {', '.join(key_columns)})",
                    row_count=duplicate_count,
                    details={'key_columns': key_columns}
                )
                self.issues.append(issue)
        else:
            # Check if any rows are completely identical
            duplicate_count = self.df.duplicated().sum()
            
            if duplicate_count > 0:
                # Exact duplicates are usually a medium severity issue
                issue = Issue(
                    check_type='duplicates',
                    severity='MEDIUM',
                    message=f"Found {duplicate_count} rows that are exact duplicates",
                    row_count=duplicate_count
                )
                self.issues.append(issue)
    
    def check_data_types(self, expected_schema=None):
        """
        Check if columns have the right data types
        Sometimes numbers get stored as text, which can cause problems
        """
        if not expected_schema:
            # If no schema is provided, just look for common problems
            for column in self.df.columns:
                dtype = str(self.df[column].dtype)
                
                # 'object' usually means text/string in pandas
                if dtype == 'object':
                    # Try to see if this text column could actually be numbers
                    try:
                        pd.to_numeric(self.df[column], errors='raise')
                        # If we get here, the column IS numeric but stored as text
                        issue = Issue(
                            check_type='data_type_suggestion',
                            severity='LOW',
                            message=f"Column '{column}' is stored as text but looks like it should be numbers",
                            column=column
                        )
                        self.issues.append(issue)
                    except:
                        # Couldn't convert to numeric, so it's probably fine as text
                        pass
        else:
            # If we have an expected schema, check if types match
            for column, expected_type in expected_schema.items():
                if column in self.df.columns:
                    actual_type = str(self.df[column].dtype)
                    if actual_type != expected_type:
                        # Type doesn't match what we expected
                        issue = Issue(
                            check_type='data_type_mismatch',
                            severity='MEDIUM',
                            message=f"Column '{column}' is '{actual_type}' but should be '{expected_type}'",
                            column=column,
                            details={'expected': expected_type, 'actual': actual_type}
                        )
                        self.issues.append(issue)
    
    def check_date_formats(self, date_columns=None):
        """
        Check if date columns are properly formatted
        Dates can be tricky - sometimes they're in weird formats that pandas can't understand
        """
        if not date_columns:
            # If not told which columns are dates, try to guess
            # Usually date columns have 'date' or 'time' in their name
            date_columns = []
            for column in self.df.columns:
                if 'date' in column.lower() or 'time' in column.lower():
                    date_columns.append(column)
        
        for column in date_columns:
            if column not in self.df.columns:
                continue  # Skip if column doesn't exist
            
            try:
                # Try to convert the column to dates
                # If this works, the dates are in a good format
                pd.to_datetime(self.df[column], errors='raise')
            except Exception as e:
                # Some dates couldn't be parsed, let's count how many
                # 'coerce' means bad dates become NaN instead of throwing errors
                parsed = pd.to_datetime(self.df[column], errors='coerce')
                
                # Count new NaNs (these were the unparseable dates)
                invalid_count = parsed.isna().sum() - self.df[column].isna().sum()
                
                if invalid_count > 0:
                    # Found some dates that can't be parsed
                    issue = Issue(
                        check_type='invalid_date_format',
                        severity='MEDIUM',
                        message=f"Column '{column}' has {invalid_count} dates that couldn't be parsed",
                        column=column,
                        row_count=invalid_count
                    )
                    self.issues.append(issue)
    
    def check_outliers(self):
        """
        Find outliers in numeric columns using standard deviation
        Outliers are values that are unusually high or low compared to the rest
        """
        # Get our threshold from config (default is 3 standard deviations)
        thresholds = self.config.get('thresholds', {})
        std_dev_threshold = thresholds.get('outlier_std_dev', 3)
        
        # Only check numeric columns (can't have outliers in text!)
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_cols:
            # Calculate the mean and standard deviation
            mean = self.df[column].mean()
            std = self.df[column].std()
            
            if std == 0:
                # If std is 0, all values are the same - no outliers possible
                continue
            
            # Find values that are more than N standard deviations away from mean
            # This is a common way to detect outliers in statistics
            outliers = self.df[
                (self.df[column] < mean - std_dev_threshold * std) |  # Too low
                (self.df[column] > mean + std_dev_threshold * std)    # Too high
            ]
            
            if len(outliers) > 0:
                outlier_percent = (len(outliers) / len(self.df)) * 100
                
                # If less than 5% are outliers, it's probably fine (LOW severity)
                # If more than 5%, that's unusual (MEDIUM severity)
                issue = Issue(
                    check_type='outliers',
                    severity='LOW' if outlier_percent < 5 else 'MEDIUM',
                    message=f"Column '{column}' has {len(outliers)} outliers ({outlier_percent:.1f}%)",
                    column=column,
                    row_count=len(outliers),
                    details={'outlier_percent': outlier_percent}
                )
                self.issues.append(issue)
    
    def check_required_columns(self):
        """
        Make sure all required columns are in the dataset
        Sometimes data is missing entire columns which can break things
        """
        required_columns = self.config.get('required_columns', [])
        
        for column in required_columns:
            if column not in self.df.columns:
                # This is a serious problem if a required column is missing
                issue = Issue(
                    check_type='missing_required_column',
                    severity='HIGH',
                    message=f"Required column '{column}' is completely missing from the data",
                    column=column
                )
                self.issues.append(issue)
    
    def check_value_ranges(self, range_rules=None):
        """
        Check if values are within expected ranges
        For example, ages should be 0-120, percentages 0-100, etc.
        """
        if not range_rules:
            return  # If no rules provided, skip this check
        
        for column, rules in range_rules.items():
            if column not in self.df.columns:
                continue  # Skip if column doesn't exist
            
            # Get the min and max values we expect
            min_val = rules.get('min')
            max_val = rules.get('max')
            
            # Create a boolean series to track which rows are out of range
            out_of_range = pd.Series([False] * len(self.df))
            
            # Check if any values are too low
            if min_val is not None:
                out_of_range |= self.df[column] < min_val
            
            # Check if any values are too high
            if max_val is not None:
                out_of_range |= self.df[column] > max_val
            
            count = out_of_range.sum()
            
            if count > 0:
                # Found some values outside the expected range
                issue = Issue(
                    check_type='value_out_of_range',
                    severity='MEDIUM',
                    message=f"Column '{column}' has {count} values outside the range [{min_val}, {max_val}]",
                    column=column,
                    row_count=count,
                    details={'min': min_val, 'max': max_val}
                )
                self.issues.append(issue)
    
    def get_summary(self):
        """
        Create a summary of all the issues found
        Useful for getting a quick overview
        """
        summary = {
            'total_issues': len(self.issues),
            'by_severity': {
                'HIGH': len([i for i in self.issues if i.severity == 'HIGH']),
                'MEDIUM': len([i for i in self.issues if i.severity == 'MEDIUM']),
                'LOW': len([i for i in self.issues if i.severity == 'LOW'])
            },
            'by_type': {}
        }
        
        # Count issues by type
        for issue in self.issues:
            if issue.check_type not in summary['by_type']:
                summary['by_type'][issue.check_type] = 0
            summary['by_type'][issue.check_type] += 1
        
        return summary


# Test the validator with some sample data
# You can run this file directly to see how it works
if __name__ == "__main__":
    # Create some sample data with problems to test the validator
    sample_data = {
        'id': [1, 2, 3, 4, 5, 2],                   # Has a duplicate (2 appears twice)
        'name': ['Alice', 'Bob', None, 'David', 'Eve', 'Bob'],  # Missing value
        'age': [25, 30, 28, 150, 35, 30],           # 150 is an outlier
        'date_joined': ['2024-01-01', '2024-02-15', 'invalid', '2024-03-20', '2024-04-10', '2024-02-15']  # 'invalid' is a bad date
    }
    df = pd.DataFrame(sample_data)
    
    # Create validator and run checks
    validator = DataValidator(df)
    issues = validator.run_all_validations()
    
    # Print all the issues we found
    print("\n=== DATA QUALITY ISSUES ===")
    for issue in issues:
        print(f"[{issue.severity}] {issue.message}")
    
    # Print a summary
    print("\n=== SUMMARY ===")
    summary = validator.get_summary()
    print(f"Total Issues: {summary['total_issues']}")
    print(f"High: {summary['by_severity']['HIGH']}, Medium: {summary['by_severity']['MEDIUM']}, Low: {summary['by_severity']['LOW']}")