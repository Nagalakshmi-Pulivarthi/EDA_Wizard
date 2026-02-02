# DataQA - Data Quality Assessment Tool

A Python tool for automated data quality validation and exploratory data analysis (EDA). Checks datasets for common quality issues and provides a risk score to assess data readiness before analysis.

---

## What It Does

DataQA validates datasets by checking for 8 common problems:
- Missing values
- Duplicate records
- Invalid data types
- Date format issues
- Statistical outliers
- Required columns
- Value range violations
- Unnamed columns

Each issue is classified by severity (HIGH, MEDIUM, LOW) and combined into a risk score from 0-100.

**You get:**
- Risk score (0-100 scale)
- Color-coded severity levels
- Interactive charts showing where problems are
- Detailed list of every issue
- Export reports in Excel, HTML, and CSV

---

## Dashboard

![Dashboard Preview](screenshots/Dashboard_screeshot.png)

![Interactive Charts](screenshots/IssuesAnalysi_screenshot.png)

![Detailed Table](screenshots/Detailed_table_screenshot.png)

---

## Installation

```bash
# Clone the repository
cd EDA_Automation

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

**Web Interface:**
```bash
streamlit run app.py
```

**Command Line:**
```bash
python run_validation.py your_data.csv
```

Reports are saved to the `outputs/` folder.

---

## Test Results

✅ **Successfully validated on real-world Kaggle datasets**

Tested on both small and large datasets with various quality issues:

| Dataset | Rows | Issues | Risk Score | Status |
|---------|------|--------|------------|--------|
| Amazon Laptops (original) | 209 | 15 | 66/100 | 🟡 HIGH |
| Amazon Laptops (corrupted) | 232 | 18 | **97/100** | 🔴 **CRITICAL** |
| Indian Toy Sales (original) | 100,000 | 12 | 40/100 | 🟢 MEDIUM |
| Indian Toy Sales (corrupted) | 100,030 | 19 | **79/100** | 🔴 **CRITICAL** |

**Performance:** 
- Small datasets (200 rows): < 1 second
- Large datasets (100K rows): ~3 seconds

**Detection Accuracy:** Tool successfully identified all data quality issues including:
- Missing values (30%+)
- Duplicate records (20%+)
- Invalid data types
- Format inconsistencies
- Statistical outliers
- Constraint violations

✅ **Tool works correctly!**

---

## Tech Stack

- Python 3.13
- Streamlit - Web interface
- Pandas - Data processing
- Plotly - Interactive visualizations
- Matplotlib & Seaborn - Charts

---

## License

MIT License

---

**Version 1.0** • February 2026
