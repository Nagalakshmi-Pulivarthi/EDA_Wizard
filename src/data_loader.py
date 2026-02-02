# data_loader.py
# Loads data from different file types (CSV, Excel, SQL)
# Handles the messy parts of reading files so you don't have to

import pandas as pd
from sqlalchemy import create_engine
import os


class DataLoader:
    """
    This class handles loading data from different sources
    Makes it easy to read CSV, Excel, or SQL databases
    """
    
    def __init__(self, source_path, source_type='csv', **kwargs):
        """
        Set up the data loader
        source_path: Path to your file (or table name if SQL)
        source_type: 'csv', 'excel', or 'sql'
        kwargs: Any extra options (like which Excel sheet to read)
        """
        self.source_path = source_path
        self.source_type = source_type.lower()
        self.kwargs = kwargs
        self.df = None  # Will store the dataframe once we load it
    
    def load(self):
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
    
    def _load_csv(self):
        """
        Load a CSV file into a pandas DataFrame
        Handles encoding issues automatically
        """
        # Check if the file exists first
        if not os.path.exists(self.source_path):
            raise FileNotFoundError(f"Can't find CSV file: {self.source_path}")
        
        # Get optional parameters (encoding and separator)
        encoding = self.kwargs.get('encoding', 'utf-8')
        sep = self.kwargs.get('sep', ',')
        
        try:
            # Try to load with UTF-8 encoding (most common)
            df = pd.read_csv(self.source_path, encoding=encoding, sep=sep)
        except UnicodeDecodeError:
            # If UTF-8 doesn't work, try latin-1 (handles special characters)
            print("UTF-8 didn't work, trying 'latin-1' encoding instead...")
            df = pd.read_csv(self.source_path, encoding='latin-1', sep=sep)
        
        return df
    
    def _load_excel(self):
        """
        Load an Excel file into a pandas DataFrame
        Can specify which sheet to read
        """
        # Check if the file exists
        if not os.path.exists(self.source_path):
            raise FileNotFoundError(f"Can't find Excel file: {self.source_path}")
        
        # Which sheet do we want? Default to the first one (0)
        sheet_name = self.kwargs.get('sheet_name', 0)
        
        df = pd.read_excel(self.source_path, sheet_name=sheet_name)
        return df
    
    def _load_sql(self):
        """
        Load data from a SQL database
        Can either read a whole table or run a custom SQL query
        """
        # We need a connection string to connect to the database
        sql_connection_string = self.kwargs.get('sql_connection_string')
        
        if not sql_connection_string:
            raise ValueError("You need to provide a sql_connection_string to load from SQL")
        
        try:
            # Create a database connection
            engine = create_engine(sql_connection_string)
            
            # Check if source_path is a SQL query or just a table name
            if self.source_path.strip().upper().startswith('SELECT'):
                # It's a SQL query, run it
                df = pd.read_sql_query(self.source_path, engine)
            else:
                # It's a table name, read the whole table
                df = pd.read_sql_table(self.source_path, engine)
            
            return df
        except Exception as e:
            raise Exception(f"Failed to load from SQL database: {str(e)}")
    
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
    
    def save_to_csv(self, output_path, index=False):
        """
        Save the dataframe to a CSV file
        Useful after cleaning the data
        """
        if self.df is None:
            raise ValueError("No data loaded yet. Call load() first.")
        
        self.df.to_csv(output_path, index=index)
        print(f"✅ Saved to {output_path}")
    
    def save_to_excel(self, output_path, sheet_name='Sheet1', index=False):
        """
        Save the dataframe to an Excel file
        Can specify which sheet name to use
        """
        if self.df is None:
            raise ValueError("No data loaded yet. Call load() first.")
        
        self.df.to_excel(output_path, sheet_name=sheet_name, index=index)
        print(f"✅ Saved to {output_path}")


# You can run this file directly to test the data loader
if __name__ == "__main__":
    # Example 1: Loading a CSV file
    print("Loading CSV file...")
    loader = DataLoader("sample_data.csv", source_type="csv")
    df = loader.load()
    print(loader.get_info())
    
    # Example 2: Loading Excel with a specific sheet
    # Uncomment to try:
    # loader = DataLoader("data.xlsx", source_type="excel", sheet_name="Sales")
    # df = loader.load()
    
    # Example 3: Loading from a SQL database
    # Uncomment and add your database connection string:
    # loader = DataLoader(
    #     "users",  # Table name
    #     source_type="sql",
    #     sql_connection_string="postgresql://user:password@localhost/mydatabase"
    # )
    # df = loader.load()
