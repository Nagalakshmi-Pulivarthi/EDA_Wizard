import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


class AutomatedEDA:
    """
    This class handles exploratory data analysis (EDA) automatically
    It loads your data, generates statistics, and creates visualizations
    """
    def __init__(self, data_source, source_type='csv', sql_conn_str=None):
        """
        Set up the EDA tool
        data_source: path to your file or SQL table name
        source_type: 'csv', 'excel', or 'sql'
        sql_conn_str: database connection string (only needed for SQL)
        """
        self.data_source = data_source
        self.source_type = source_type
        self.sql_conn_str = sql_conn_str
        self.df = None  # Will store the dataframe after loading

    def load_data(self):
        """
        Load the data based on what type of file it is
        Handles CSV, Excel, and SQL sources
        """
        # Load based on source type
        if self.source_type == 'csv':
            self.df = pd.read_csv(self.data_source)
        elif self.source_type == 'excel':
            self.df = pd.read_excel(self.data_source)
        elif self.source_type == 'sql':
            if not self.sql_conn_str:
                raise ValueError("Need a SQL connection string to load from database")
            engine = create_engine(self.sql_conn_str)
            self.df = pd.read_sql_table(self.data_source, engine)
        else:
            raise ValueError("source_type must be 'csv', 'excel', or 'sql'")
        
        # Fix a weird Streamlit compatibility issue with certain integer types
        # Some pandas integer types don't work well with Streamlit, so convert them
        for col in self.df.columns:
            dtype_str = str(self.df[col].dtype)
            # Check if it's one of these problematic types
            if dtype_str in ['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32', 'UInt64']:
                # Convert to regular float (this works everywhere)
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').astype('float64')
        
        print("✅ Data loaded successfully!")
        print(f"Shape: {self.df.shape}")
        return self.df

    def basic_stats(self):
        """
        Print basic statistics about the data
        Shows info, summary statistics, and value counts for categorical columns
        """
        print("\n=== Dataset Info ===")
        print(self.df.info())
        
        print("\n=== Numeric Summary ===")
        print(self.df.describe())  # Mean, median, std, etc. for numbers
        
        print("\n=== Categorical Summary ===")
        # For text columns, show the most common values
        for col in self.df.select_dtypes(include='object').columns:
            print(f"\n-- {col} --")
            print(self.df[col].value_counts())

    def data_quality_check(self):
        """
        Check the quality of the data
        Looks for missing values, duplicates, and outliers
        """
        print("\n=== Missing Values ===")
        print(self.df.isna().sum())  # Count missing values in each column
        
        print("\n=== Duplicates ===")
        print(f"Total duplicates: {self.df.duplicated().sum()}")

        # Check for outliers using IQR method (Interquartile Range)
        print("\n=== Outlier Detection ===")
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        
        for col in numeric_cols:
            # Calculate Q1 (25th percentile) and Q3 (75th percentile)
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Values below Q1-1.5*IQR or above Q3+1.5*IQR are considered outliers
            # This is a standard statistical method
            outliers = self.df[(self.df[col] < Q1 - 1.5*IQR) | (self.df[col] > Q3 + 1.5*IQR)]
            print(f"{col}: {len(outliers)} potential outliers")

    def visualize(self, save_plots=False):
        """
        Create visualizations to understand the data better
        Makes histograms, bar charts, and a correlation heatmap
        """
        # Histograms for all numeric columns
        # Shows the distribution of values
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        self.df[numeric_cols].hist(figsize=(12,10))
        if save_plots:
            plt.savefig("histograms.png")
        plt.show()

        # Bar plots for categorical (text) columns
        # Shows the count of each category
        categorical_cols = self.df.select_dtypes(include='object').columns
        for col in categorical_cols:
            plt.figure(figsize=(8,4))
            sns.countplot(data=self.df, x=col)
            plt.xticks(rotation=45)  # Rotate labels so they don't overlap
            if save_plots:
                plt.savefig(f"{col}_barplot.png")
            plt.show()

        # Correlation heatmap shows which numeric columns are related
        # Darker colors = stronger correlation
        plt.figure(figsize=(10,8))
        sns.heatmap(self.df.corr(), annot=True, cmap='coolwarm')
        if save_plots:
            plt.savefig("correlation_heatmap.png")
        plt.show()

    def export_summary(self, excel_path="EDA_Summary.xlsx", html_report=False):
        """
        Export all the analysis to an Excel file
        Creates separate sheets for different types of summaries
        """
        # Create an Excel file with multiple sheets
        with pd.ExcelWriter(excel_path) as writer:
            # Sheet 1: Summary statistics for numeric columns
            self.df.describe().to_excel(writer, sheet_name='Numeric_Summary')
            
            # Sheet 2+: Value counts for each text column
            for col in self.df.select_dtypes(include='object').columns:
                # Clean up the column name to make it a valid Excel sheet name
                # Excel doesn't like special characters in sheet names
                safe_name = col.replace(':', '_').replace('*', '_').replace('?', '_')
                safe_name = safe_name.replace('/', '_').replace('\\', '_').replace('[', '_').replace(']', '_')
                # Keep it short (Excel has a 31 character limit for sheet names)
                safe_name = safe_name[:24]
                
                self.df[col].value_counts().to_excel(writer, sheet_name=f"{safe_name}_Counts")
            
            # Last sheet: Missing value counts
            self.df.isna().sum().to_excel(writer, sheet_name='Missing_Values')
            
        print(f"✅ Excel summary saved to {excel_path}")



# Test the EDA tool by running this file directly
if __name__ == "__main__":
    # Example: Load and analyze a CSV file
    print("Running automated EDA on sample data...")
    
    eda = AutomatedEDA(
        data_source="sample_data.csv",  # Replace with your file path
        source_type="csv"
    )
    
    # Load the data
    df = eda.load_data()
    
    # Run the analysis
    eda.basic_stats()           # Print statistics
    eda.data_quality_check()    # Check for problems
    eda.visualize(save_plots=True)  # Create charts
    eda.export_summary(excel_path="EDA_Summary.xlsx")  # Save results