import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


class AutomatedEDA:
    def __init__(self, data_source, source_type='csv', sql_conn_str=None):
        """
        data_source: path to CSV/Excel file or SQL table name
        source_type: 'csv', 'excel', 'sql'
        sql_conn_str: SQLAlchemy connection string (for SQL source)
        """
        self.data_source = data_source
        self.source_type = source_type
        self.sql_conn_str = sql_conn_str
        self.df = None

    def load_data(self):
        if self.source_type == 'csv':
            self.df = pd.read_csv(self.data_source)
        elif self.source_type == 'excel':
            self.df = pd.read_excel(self.data_source)
        elif self.source_type == 'sql':
            if not self.sql_conn_str:
                raise ValueError("SQL connection string required for SQL source")
            engine = create_engine(self.sql_conn_str)
            self.df = pd.read_sql_table(self.data_source, engine)
        else:
            raise ValueError("source_type must be 'csv', 'excel', or 'sql'")
        
        # Fix PyArrow compatibility: Convert nullable integer types to regular types
        # This prevents Arrow serialization errors in Streamlit
        for col in self.df.columns:
            dtype_str = str(self.df[col].dtype)
            # Check for nullable integer types (Int8, Int16, Int32, Int64, etc.)
            if dtype_str in ['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32', 'UInt64']:
                # Convert to regular float to preserve NaN values
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').astype('float64')
        
        print("Data loaded successfully!")
        print(f"Shape: {self.df.shape}")
        return self.df

    def basic_stats(self):
        print("\n=== Dataset Info ===")
        print(self.df.info())
        print("\n=== Numeric Summary ===")
        print(self.df.describe())
        print("\n=== Categorical Summary ===")
        for col in self.df.select_dtypes(include='object').columns:
            print(f"\n-- {col} --")
            print(self.df[col].value_counts())

    def data_quality_check(self):
        print("\n=== Missing Values ===")
        print(self.df.isna().sum())
        print("\n=== Duplicates ===")
        print(f"Total duplicates: {self.df.duplicated().sum()}")

        # Optional: basic outlier detection using IQR
        print("\n=== Outlier Detection ===")
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[col] < Q1 - 1.5*IQR) | (self.df[col] > Q3 + 1.5*IQR)]
            print(f"{col}: {len(outliers)} potential outliers")

    def visualize(self, save_plots=False):
        # Histograms for numeric columns
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        self.df[numeric_cols].hist(figsize=(12,10))
        if save_plots:
            plt.savefig("histograms.png")
        plt.show()

        # Bar plots for categorical columns
        categorical_cols = self.df.select_dtypes(include='object').columns
        for col in categorical_cols:
            plt.figure(figsize=(8,4))
            sns.countplot(data=self.df, x=col)
            plt.xticks(rotation=45)
            if save_plots:
                plt.savefig(f"{col}_barplot.png")
            plt.show()

        # Correlation heatmap
        plt.figure(figsize=(10,8))
        sns.heatmap(self.df.corr(), annot=True, cmap='coolwarm')
        if save_plots:
            plt.savefig("correlation_heatmap.png")
        plt.show()

    def export_summary(self, excel_path="EDA_Summary.xlsx", html_report=False):
    # Export to Excel
     with pd.ExcelWriter(excel_path) as writer:
        self.df.describe().to_excel(writer, sheet_name='Numeric_Summary')
        for col in self.df.select_dtypes(include='object').columns:
            # Sanitize sheet name - remove invalid Excel characters
            safe_name = col.replace(':', '_').replace('*', '_').replace('?', '_').replace('/', '_').replace('\\', '_').replace('[', '_').replace(']', '_')
            # Limit to 24 chars (leaving room for "_Counts" suffix, total 31)
            safe_name = safe_name[:24]
            self.df[col].value_counts().to_excel(writer, sheet_name=f"{safe_name}_Counts")
        self.df.isna().sum().to_excel(writer, sheet_name='Missing_Values')
        print(f"Excel summary saved to {excel_path}")



# === USAGE EXAMPLE ===
if __name__ == "__main__":
    # CSV example
    eda = AutomatedEDA(data_source="C:/Users/nagal/Downloads/surveyed_transects_data_20260105.csv", source_type="csv")
    df = eda.load_data()
    eda.basic_stats()
    eda.data_quality_check()
    eda.visualize(save_plots=True)
    eda.export_summary(excel_path="EDA_Summary.xlsx", html_report=True)