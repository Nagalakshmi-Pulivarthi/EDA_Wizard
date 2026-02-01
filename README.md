# 📊 Automated EDA & Data Validation Tool

A comprehensive Python tool for automated Exploratory Data Analysis (EDA) and data quality validation. Features both a Streamlit web interface and a powerful command-line validation pipeline with risk assessment.

## ✨ Features

### 🎯 Two Ways to Use:

#### 1. **Streamlit Web App** (Interactive EDA)
- **📁 File Upload**: Support for CSV and Excel files
- **📊 Dataset Overview**: Quick metrics and data preview
- **📈 Summary Statistics**: Comprehensive statistical analysis
- **🔥 Correlation Heatmap**: Visual correlation analysis
- **💾 Export Reports**: Download Excel reports

#### 2. **Validation Pipeline** (Data Quality & Risk Assessment)
- **🔍 Comprehensive Validation**: 8 different data quality checks
- **⚠️ Risk Scoring**: Automated risk assessment (0-100 scale)
- **📊 Multiple Reports**: CSV, Excel, HTML, and text summaries
- **🎯 Smart Recommendations**: Actionable insights to fix issues
- **📈 Detailed Analysis**: Missing values, duplicates, outliers, data types, dates, and more

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

### Option 1: Enhanced Streamlit Web App (Interactive)

**New!** The Streamlit app now has 3 powerful modes:

```bash
streamlit run app.py
```

Then choose your analysis mode:
1. **📈 Quick EDA** - Fast data exploration with visualizations
2. **🔍 Data Validation** - Comprehensive quality checks with risk scoring
3. **📊 Complete Analysis** - Combined EDA + Validation in one view

**Features**:
- ✨ Color-coded risk assessment
- ✨ Interactive issue explorer with filters
- ✨ Visual dashboards and charts
- ✨ One-click report downloads
- ✨ Smart recommendations
- ✨ Professional UI

See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for detailed instructions.

### Option 2: Validation Pipeline (Data Quality Assessment)

#### Quick Start - Single Command:
```bash
python run_validation.py your_data.csv
```

That's it! This will:
- Load your data
- Run 8 validation checks
- Calculate risk score
- Generate 4 different reports

#### Advanced Usage:
```python
from src import DataLoader, DataValidator, RiskEngine, ReportGenerator

# Load data
loader = DataLoader("data.csv", source_type="csv")
df = loader.load()

# Run validations
validator = DataValidator(df)
issues = validator.run_all_validations()

# Calculate risk
risk_engine = RiskEngine()
risk_score = risk_engine.calculate_risk(issues, df)

# Generate reports
reporter = ReportGenerator(df, issues, risk_score)
reporter.generate_all_reports()
```

#### What Gets Checked:
1. ✅ **Missing Values** - Column and row level analysis
2. ✅ **Duplicates** - Full row and key column duplicates
3. ✅ **Data Types** - Type validation and suggestions
4. ✅ **Date Formats** - Invalid date detection
5. ✅ **Outliers** - Statistical outlier detection
6. ✅ **Required Columns** - Ensure critical columns exist
7. ✅ **Value Ranges** - Min/max validation
8. ✅ **Risk Scoring** - Overall data quality assessment

## 📂 Project Structure

```
EDA_Automation/
├── app.py                      # Streamlit web interface
├── main.py                     # Core EDA logic (AutomatedEDA class)
├── run_validation.py           # Main validation pipeline script
├── requirements.txt            # Package dependencies
├── config/
│   └── rules.json             # Validation rules and thresholds
├── src/                       # Core validation modules
│   ├── __init__.py           # Package initialization
│   ├── data_loader.py        # Data loading from CSV/Excel/SQL
│   ├── validators.py         # All validation checks
│   ├── risk_engine.py        # Risk scoring and assessment
│   └── report_generator.py   # Report generation (CSV/Excel/HTML)
├── outputs/                   # Generated reports (auto-created)
│   ├── validation_report.csv
│   ├── validation_report.xlsx
│   ├── validation_report.html
│   └── risk_summary.txt
└── README.md                  # This file
```

## 🔧 Features Breakdown

### 1. Data Loader (`src/data_loader.py`)
Load data from multiple sources:
```python
from src import DataLoader

# CSV
loader = DataLoader("data.csv", source_type="csv")

# Excel (with sheet selection)
loader = DataLoader("data.xlsx", source_type="excel", sheet_name="Sales")

# SQL
loader = DataLoader("users", source_type="sql", 
                   sql_connection_string="postgresql://localhost/db")

df = loader.load()
```

### 2. Data Validator (`src/validators.py`)
Run comprehensive validation checks:
```python
from src import DataValidator

validator = DataValidator(df, config_path="config/rules.json")
issues = validator.run_all_validations()

# Or run specific checks
validator.check_missing_values_column()
validator.check_duplicates(key_columns=['id'])
validator.check_date_formats(date_columns=['created_at'])
validator.check_outliers()
```

### 3. Risk Engine (`src/risk_engine.py`)
Calculate data quality risk:
```python
from src import RiskEngine

risk_engine = RiskEngine()
risk_score = risk_engine.calculate_risk(issues, df)

print(f"Risk Level: {risk_score.risk_level}")  # LOW, MEDIUM, HIGH, CRITICAL
print(f"Risk Score: {risk_score.total_score}/100")
print(risk_score.recommendations)
```

### 4. Report Generator (`src/report_generator.py`)
Generate beautiful reports:
```python
from src import ReportGenerator

reporter = ReportGenerator(df, issues, risk_score)

# Generate specific report types
reporter.generate_csv_report()
reporter.generate_excel_report()
reporter.generate_html_report()  # Opens in browser
reporter.print_console_summary()

# Or generate all at once
reporter.generate_all_reports(output_dir="outputs")
```

### 5. Streamlit App (Classic EDA)
```python
from main import AutomatedEDA

eda = AutomatedEDA(data_source="data.csv", source_type="csv")
df = eda.load_data()
eda.basic_stats()
eda.data_quality_check()
eda.visualize(save_plots=True)
eda.export_summary(excel_path="report.xlsx")
```

## 📊 Report Outputs

### Validation Reports Include:

#### 1. **CSV Report** (`validation_report.csv`)
Simple tabular format with all issues

#### 2. **Excel Report** (`validation_report.xlsx`)
Multi-sheet workbook:
- **Summary**: Overview of dataset and issues
- **Issues**: Detailed list of all problems found
- **Data Overview**: Column-by-column analysis
- **Recommendations**: Prioritized action items

#### 3. **HTML Report** (`validation_report.html`)
Beautiful, styled report with:
- Visual metrics dashboard
- Color-coded severity levels
- Interactive tables
- Risk assessment summary

#### 4. **Risk Summary** (`risk_summary.txt`)
Text-based risk assessment with:
- Overall risk score and level
- Issue breakdown by severity
- Detailed recommendations
- Full issue listing

### Classic EDA Report (Streamlit/main.py):
1. **Numeric_Summary**: Descriptive statistics
2. **[Column]_Counts**: Value counts for categorical columns
3. **Missing_Values**: Missing data analysis

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

### Example 1: Quick Validation
```bash
# Validate any CSV file
python run_validation.py sales_data.csv

# Validate Excel file
python run_validation.py customer_data.xlsx excel
```

### Example 2: Custom Validation with Python
```python
from src import DataLoader, DataValidator, RiskEngine, ReportGenerator

# Load data
loader = DataLoader("sales_data.csv", source_type="csv")
df = loader.load()

# Run specific validations
validator = DataValidator(df)
validator.check_missing_values_column()
validator.check_duplicates(key_columns=['order_id'])
validator.check_value_ranges({'age': {'min': 0, 'max': 120}})

# Get issues
issues = validator.issues

# Calculate risk
risk_engine = RiskEngine()
risk_score = risk_engine.calculate_risk(issues, df)

# Generate reports
reporter = ReportGenerator(df, issues, risk_score)
reporter.generate_html_report()  # Beautiful HTML report
```

### Example 3: Classic EDA with Streamlit
```python
from main import AutomatedEDA

eda = AutomatedEDA(data_source="sales_data.csv", source_type="csv")
df = eda.load_data()
eda.basic_stats()
eda.data_quality_check()
eda.visualize(save_plots=True)
eda.export_summary(excel_path="sales_analysis.xlsx")
```

### Example 4: Integrate with SQL
```python
from src import DataLoader

conn_str = "postgresql://user:password@localhost:5432/mydb"
loader = DataLoader("customers", source_type="sql", 
                   sql_connection_string=conn_str)
df = loader.load()

# Then run validations as usual...
```

## 🎨 Configuration

Edit `config/rules.json` to customize validation rules:

```json
{
  "critical_columns": ["id", "email"],
  "required_columns": ["name", "created_at"],
  "risk_weights": {
    "missing_critical_id": {
      "severity": "HIGH",
      "points": 5
    },
    "duplicate_primary_key": {
      "severity": "HIGH",
      "points": 5
    }
  },
  "thresholds": {
    "missing_percent_high": 30,
    "missing_percent_medium": 10,
    "outlier_std_dev": 3
  }
}
```

## 📝 Future Enhancements

- [x] Comprehensive data validation engine
- [x] Risk scoring and assessment
- [x] Multiple report formats (CSV, Excel, HTML)
- [x] Configurable validation rules
- [ ] Add validation to Streamlit interface
- [ ] Support for more file formats (JSON, Parquet, TSV)
- [ ] Interactive data filtering
- [ ] Time series validation
- [ ] Data profiling with pandas-profiling
- [ ] PDF report generation
- [ ] Data comparison (before/after)
- [ ] Automated data cleaning suggestions
- [ ] Machine learning readiness checks

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

## 🎓 What You'll Learn

This project demonstrates:
- Clean, maintainable Python code structure
- Modular design with reusable components
- Data validation best practices
- Risk assessment methodologies
- Report generation in multiple formats
- Configuration-driven validation
- Simple but effective data classes with `@dataclass`

**Version**: 1.0.0  
**Last Updated**: January 2026

## ❓ FAQ

**Q: Which approach should I use - Streamlit or validation pipeline?**
A: Use Streamlit for quick interactive EDA. Use validation pipeline for comprehensive data quality assessment before critical analysis.

**Q: Can I use both together?**
A: Absolutely! They complement each other. Use validation pipeline first to assess quality, then Streamlit for visual exploration.

**Q: How do I customize validation rules?**
A: Edit `config/rules.json` to set thresholds, add required columns, and adjust risk weights.

**Q: What's the difference between severity and risk score?**
A: Severity (HIGH/MEDIUM/LOW) is per-issue. Risk score (0-100) is overall dataset quality based on all issues combined.
