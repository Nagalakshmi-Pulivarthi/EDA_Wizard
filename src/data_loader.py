# data_loader.py
# Module for loading data from various sources (CSV, Excel, SQL)

import pandas as pd
from sqlalchemy import create_engine
from typing import Optional, Dict, Any
import os


class DataLoader:
    """
    Simple data loader that handles CSV, Excel, and SQL sources
    """
    
    def __init__(self, source_path: str, source_type: str = 'csv', **kwargs):
        """
        Initialize data loader
        
        Args:
            source_path: Path to file or SQL table name
            source_type: One of 'csv', 'excel', 'sql'
            **kwargs: Additional arguments (sql_connection_string, sheet_name, etc.)
        """
        self.source_path = source_path
        self.source_type = source_type.lower()
        self.kwargs = kwargs
        self.df = None
    
    def load(self) -> pd.DataFrame:
        """
        Load data from the specified source
        
        Returns:
            pandas DataFrame with the loaded data
        """
        print(f"Loading data from {self.source_type} source...")
        
        if self.source_type == 'csv':
            self.df = self._load_csv()
        elif self.source_type == 'excel':
            self.df = self._load_excel()
        elif self.source_type == 'sql':
            self.df = self._load_sql()
        else:
            raise ValueError(f"Unsupported source_type: {self.source_type}. Use 'csv', 'excel', or 'sql'")
        
        print(f"✅ Data loaded successfully! Shape: {self.df.shape}")
        return self.df
    
    def _load_csv(self) -> pd.DataFrame:
        """Load data from CSV file"""
        if not os.path.exists(self.source_path):
            raise FileNotFoundError(f"CSV file not found: {self.source_path}")
        
        # Get optional parameters
        encoding = self.kwargs.get('encoding', 'utf-8')
        sep = self.kwargs.get('sep', ',')
        
        try:
            df = pd.read_csv(self.source_path, encoding=encoding, sep=sep)
        except UnicodeDecodeError:
            # Try different encoding if UTF-8 fails
            print("UTF-8 encoding failed, trying 'latin-1'...")
            df = pd.read_csv(self.source_path, encoding='latin-1', sep=sep)
        
        return df
    
    def _load_excel(self) -> pd.DataFrame:
        """Load data from Excel file"""
        if not os.path.exists(self.source_path):
            raise FileNotFoundError(f"Excel file not found: {self.source_path}")
        
        # Get optional parameters
        sheet_name = self.kwargs.get('sheet_name', 0)  # Default to first sheet
        
        df = pd.read_excel(self.source_path, sheet_name=sheet_name)
        return df
    
    def _load_sql(self) -> pd.DataFrame:
        """Load data from SQL database"""
        sql_connection_string = self.kwargs.get('sql_connection_string')
        
        if not sql_connection_string:
            raise ValueError("sql_connection_string is required for SQL source type")
        
        try:
            engine = create_engine(sql_connection_string)
            
            # Check if source_path is a table name or SQL query
            if self.source_path.strip().upper().startswith('SELECT'):
                # It's a SQL query
                df = pd.read_sql_query(self.source_path, engine)
            else:
                # It's a table name
                df = pd.read_sql_table(self.source_path, engine)
            
            return df
        except Exception as e:
            raise Exception(f"Failed to load data from SQL: {str(e)}")
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get basic information about the loaded dataset
        
        Returns:
            Dictionary with dataset info
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")
        
        info = {
            'shape': self.df.shape,
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'column_names': list(self.df.columns),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / (1024 * 1024),
            'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        }
        
        return info
    
    def save_to_csv(self, output_path: str, index: bool = False):
        """Save the loaded data to a CSV file"""
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")
        
        self.df.to_csv(output_path, index=index)
        print(f"Data saved to {output_path}")
    
    def save_to_excel(self, output_path: str, sheet_name: str = 'Sheet1', index: bool = False):
        """Save the loaded data to an Excel file"""
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")
        
        self.df.to_excel(output_path, sheet_name=sheet_name, index=index)
        print(f"Data saved to {output_path}")


# Example usage
if __name__ == "__main__":
    # Example 1: Load CSV
    loader = DataLoader("sample_data.csv", source_type="csv")
    df = loader.load()
    print(loader.get_info())
    
    # Example 2: Load Excel with specific sheet
    # loader = DataLoader("data.xlsx", source_type="excel", sheet_name="Sales")
    # df = loader.load()
    
    # Example 3: Load from SQL
    # loader = DataLoader(
    #     "users",
    #     source_type="sql",
    #     sql_connection_string="postgresql://user:pass@localhost/db"
    # )
    # df = loader.load()
