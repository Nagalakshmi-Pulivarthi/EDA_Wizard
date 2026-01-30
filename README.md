# 📊 Automated EDA Tool

A Streamlit-based web application for automated Exploratory Data Analysis (EDA). Upload your CSV or Excel files and get instant insights with interactive visualizations and statistical summaries.

## ✨ Features

- **📁 File Upload**: Support for CSV and Excel (.xlsx, .xls) files
- **📊 Dataset Overview**: Quick metrics showing rows, columns, and duplicates
- **📈 Summary Statistics**: Comprehensive statistical analysis for all numeric columns
- **🔍 Data Quality Check**: 
  - Missing values detection
  - Data type information
  - Duplicate row identification
- **🔥 Correlation Heatmap**: Visual representation of correlations between numeric features
- **💾 Export Reports**: Generate and download detailed Excel reports with multiple sheets

## 🚀 Installation

### Prerequisites

- Python 3.13.x
- pip (Python package manager)

### Setup Steps

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   py -3.13 -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows Command Prompt
   .\venv\Scripts\activate.bat
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Dependencies

- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `seaborn` - Statistical data visualization
- `matplotlib` - Plotting library
- `sqlalchemy` - SQL database connectivity (for future SQL support)
- `openpyxl` - Excel file handling
- `streamlit` - Web app framework

## 🎯 Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to `http://localhost:8501` (opens automatically)

3. **Upload your data**:
   - Click "Browse files" or drag-and-drop
   - Select a CSV or Excel file

4. **Explore your data**:
   - View dataset overview and preview
   - Check summary statistics
   - Identify data quality issues
   - Analyze correlations with the heatmap

5. **Export results**:
   - Click "Generate Excel Report"
   - Download the comprehensive Excel file with multiple analysis sheets

## 📂 Project Structure

```
DataPrpject/
├── app.py              # Streamlit web interface
├── main.py             # Core EDA logic (AutomatedEDA class)
├── requirements.txt    # Package dependencies
└── README.md           # This file
```

## 🔧 Features Breakdown

### AutomatedEDA Class (main.py)

The core class supports three data source types:

- **CSV files**: `source_type='csv'`
- **Excel files**: `source_type='excel'`
- **SQL databases**: `source_type='sql'` (with connection string)

### Available Methods

```python
from main import AutomatedEDA

# Create instance
eda = AutomatedEDA(data_source="data.csv", source_type="csv")

# Load data
df = eda.load_data()

# Display basic statistics
eda.basic_stats()

# Check data quality
eda.data_quality_check()

# Create visualizations
eda.visualize(save_plots=True)

# Export summary report
eda.export_summary(excel_path="report.xlsx")
```

## 📊 Excel Report Contents

The generated Excel report includes:

1. **Numeric_Summary**: Descriptive statistics for all numeric columns
2. **[Column]_Counts**: Value counts for each categorical column (sanitized names)
3. **Missing_Values**: Count of missing values per column

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `streamlit: command not found`
- **Solution**: Make sure your virtual environment is activated and streamlit is installed

**Issue**: `ModuleNotFoundError: No module named 'pandas'`
- **Solution**: Install required packages: `pip install -r requirements.txt`

**Issue**: `ValueError: Invalid character found in sheet title`
- **Solution**: This is handled automatically - column names with special characters are sanitized

**Issue**: Python 3.14 compatibility errors with certain packages
- **Solution**: Use Python 3.13 instead (recommended version)

**Issue**: PyArrow build errors during installation
- **Solution**: Python 3.13 is recommended for better package compatibility

## 🎨 Customization

You can easily customize the tool by modifying:

- **`app.py`**: Change the UI, add new visualizations, modify layout
- **`main.py`**: Add new analysis methods, modify export format
- **Colors**: Change the heatmap colormap in `app.py` line 54 (`cmap='coolwarm'`)
- **Metrics**: Add custom metrics to the dataset overview section

## 💡 Usage Examples

### Analyze a CSV file
```python
from main import AutomatedEDA

eda = AutomatedEDA(data_source="sales_data.csv", source_type="csv")
df = eda.load_data()
eda.basic_stats()
eda.data_quality_check()
eda.export_summary(excel_path="sales_analysis.xlsx")
```

### Analyze an Excel file
```python
eda = AutomatedEDA(data_source="customer_data.xlsx", source_type="excel")
df = eda.load_data()
eda.visualize(save_plots=True)
```

### Connect to SQL Database
```python
conn_str = "postgresql://user:password@localhost:5432/mydb"
eda = AutomatedEDA(
    data_source="customers",  # table name
    source_type="sql",
    sql_conn_str=conn_str
)
df = eda.load_data()
```

## 📝 Future Enhancements

- [ ] Add database connectivity support in Streamlit interface
- [ ] Support for more file formats (JSON, Parquet, TSV)
- [ ] Interactive data filtering and column selection
- [ ] Advanced outlier detection with visualization
- [ ] Time series analysis features
- [ ] Data profiling reports with sweetviz integration
- [ ] PDF report generation
- [ ] Data comparison (before/after cleaning)
- [ ] Missing data imputation suggestions
- [ ] Automated insight generation

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Created as a Python data analysis automation tool for quick and efficient exploratory data analysis.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data analysis powered by [Pandas](https://pandas.pydata.org/)
- Visualizations using [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/)
- Statistical computing with [NumPy](https://numpy.org/)

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)

---

**Note**: This tool is designed for quick exploratory data analysis. For production-grade analysis, consider additional validation, testing, and data governance practices.

**Version**: 1.0.0  
**Last Updated**: January 2026
