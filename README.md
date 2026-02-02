# DataQA - Your Data Quality Assistant 🎯

**Make sure your data is ready before you analyze it.**

DataQA is a powerful Python tool that automatically checks your data for common problems - missing values, duplicates, formatting issues, and more. It gives you a clear quality score and tells you exactly what to fix, all through an interactive dashboard.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Key Features

- **🎯 Automated Risk Assessment** - Get a 0-100 risk score instantly
- **📊 Interactive Visualizations** - Explore data quality with interactive charts
- **🔍 8 Comprehensive Checks** - Missing values, duplicates, outliers, and more
- **📈 Column-Level Analysis** - See which columns have the most issues
- **🎨 Beautiful Dashboard** - Professional Streamlit interface
- **💾 Multiple Export Formats** - HTML, Excel, CSV reports
- **⚡ Fast Processing** - Handles datasets with 100K+ rows
- **🔧 Customizable Rules** - Adjust thresholds via JSON config

---

## 📸 Dashboard Preview

### Risk Assessment Dashboard
> *Upload a dataset and get instant quality insights*

![Dashboard Preview](screenshots/dashboard_full.png)
*Full dashboard showing Risk Score (97/100 - CRITICAL) with 18 issues detected*

### Interactive Visualizations
> *Three powerful charts to understand your data quality*

![Interactive Charts](screenshots/charts_overview.png)
*Issues by Severity, Column, and Type - all interactive with hover details*

### Detailed Issue Reporting
> *See every issue with color-coded severity levels*

![Detailed Table](screenshots/detailed_table.png)
*Comprehensive table with export to CSV functionality*

### Before/After Comparison
> *Real-world example showing DataQA's detection capabilities*

| Dataset | Rows | Issues | Risk Score | Status |
|---------|------|--------|------------|--------|
| Amazon Laptops (Clean) | 209 | 15 | 66/100 | 🟡 HIGH |
| Amazon Laptops (Corrupted) | 232 | 18 | **97/100** | 🔴 **CRITICAL** |
| Indian Toy Sales (Clean) | 100,000 | 12 | 40/100 | 🟡 MEDIUM |
| Indian Toy Sales (Corrupted) | 100,030 | 19 | **79/100** | 🔴 **CRITICAL** |

*DataQA successfully identified data quality degradation across different dataset sizes*

---

## Why Use DataQA?

Ever loaded a dataset only to find:
- ❌ Half the values are missing?
- ❌ Duplicate records everywhere?
- ❌ Dates in weird formats?
- ❌ "Unnamed" columns with no idea what they mean?
- ❌ Outliers that skew your analysis?

**✅ DataQA catches these problems before they ruin your analysis.**

---

## What Does It Do?

DataQA checks your data and gives you:

✅ **Risk Score** - A simple 0-100 score (lower is better)  
✅ **Quality Issues** - Clear list of what's wrong with severity levels  
✅ **Recommendations** - What to fix first based on risk level  
✅ **Visual Reports** - Interactive charts and downloadable tables  
✅ **Column Analysis** - Which columns need attention  
✅ **Issue Breakdown** - By type and severity

Plus, you get basic stats, correlation heatmaps, and comprehensive EDA features.

---

## Getting Started

### 1. Install Python
You need Python 3.13 or newer. [Download here](https://www.python.org/downloads/)

### 2. Install DataQA

Open your terminal and run:

```bash
# Clone or download this project
cd EDA_Automation

# Install required packages
pip install -r requirements.txt
```

That's it! You're ready to go.

---

## How to Use It

### Web Interface (Easiest Way)

Run this command:
```bash
streamlit run app.py
```

Your browser will open automatically. Then:
1. Upload your CSV or Excel file
2. See your data quality score instantly
3. Review the issues found
4. Download detailed reports

**That's it!** No coding required.

---

### Command Line (For Automation)

Want to check a file quickly? Run:
```bash
python run_validation.py your_data.csv
```

This will:
- Check your data for 8 common issues
- Calculate a quality score
- Generate reports in multiple formats
- Save everything to the `outputs/` folder

---

## 🔍 What Gets Checked?

DataQA performs **8 comprehensive validation checks** on your dataset:

| Check | What It Does | Severity Levels |
|-------|--------------|----------------|
| 🔴 **Missing Values** | Finds blank/null cells in your data | HIGH: >30%, MEDIUM: 10-30%, LOW: <10% |
| 🔴 **Duplicates** | Catches repeated rows (exact matches) | HIGH: >10%, MEDIUM: 5-10%, LOW: <5% |
| 🟡 **Data Types** | Ensures numbers are numbers, dates are dates | HIGH: Critical columns, MEDIUM: Others |
| 🟡 **Date Formats** | Finds invalid or inconsistent dates | HIGH: Unparseable, MEDIUM: Inconsistent |
| 🟠 **Outliers** | Spots extreme values using statistical methods | HIGH: >3 std dev, MEDIUM: >2 std dev |
| 🟢 **Required Columns** | Checks if important columns exist | HIGH: Missing required, LOW: Optional |
| 🟡 **Value Ranges** | Validates values are within expected limits | HIGH: Out of range, MEDIUM: Edge cases |
| 🔵 **Unnamed Columns** | Detects columns with generic names | LOW: Needs renaming |

### Risk Scoring Algorithm

Each issue is weighted by:
- **Severity** (HIGH=3, MEDIUM=2, LOW=1)
- **Impact** (percentage of data affected)
- **Column importance** (from config)

Final score: `(Sum of weighted issues / Maximum possible score) × 100`

---

## 📊 Understanding Your Risk Score

After checking your data, DataQA gives you a risk score with actionable recommendations:

| Score | Level | Indicator | What It Means | Action |
|-------|-------|-----------|---------------|--------|
| **0-24** | 🟢 **LOW** | Green | Your data is good to go | Minor cleanup optional |
| **25-49** | 🟡 **MEDIUM** | Yellow | Some issues to fix, but usable | Review and fix key issues |
| **50-74** | 🟠 **HIGH** | Orange | Serious problems - fix before analyzing | Must fix before analysis |
| **75-100** | 🔴 **CRITICAL** | Red | Too many issues - don't use this data yet | Extensive cleanup required |

### What Each Level Includes:

**🟢 LOW (0-24)**
- Few missing values (<10%)
- No duplicates or minimal (<2%)
- Clean data types
- Ready for analysis

**🟡 MEDIUM (25-49)**
- Some missing data (10-30%)
- Minor format inconsistencies
- A few outliers
- Usable with caution

**🟠 HIGH (50-74)**
- Significant missing data (>30%)
- Multiple duplicates (>5%)
- Type mismatches
- Needs cleanup first

**🔴 CRITICAL (75-100)**
- Extensive data quality issues
- Many HIGH severity problems
- Invalid data types throughout
- **Do not analyze** until fixed

---

## What You Get

DataQA generates several reports for you:

### 1. Interactive Plotly Dashboard (NEW!)
- **Fully interactive** - Click, zoom, and explore your data quality
- Beautiful visualizations (gauge charts, bar charts, tables)
- **Perfect for sharing** - Open in any browser, no software needed
- **Great for LinkedIn/Portfolio** - Shows your data quality work professionally
- File: `outputs/interactive_dashboard.html`

### 2. Web Dashboard (Streamlit)
- Interactive charts
- Color-coded issues
- One-click downloads

### 3. Excel Report
- Summary sheet with your score
- Detailed issues list
- Column-by-column breakdown
- Recommendations

### 4. HTML Report
- Beautiful styled report
- Easy to share with your team
- Opens in any browser

### 5. CSV Files
- Simple tables for further analysis
- Import into Excel or other tools

---

## Project Files

```
EDA_Automation/
├── app.py                    # Web interface (run this!)
├── run_validation.py         # Command-line tool
├── requirements.txt          # What to install
├── config/
│   └── rules.json           # Customize validation rules here
├── src/                     # Core code (you don't need to touch this)
├── outputs/                 # Your reports go here
└── tests/data/              # Sample datasets for testing
```

## 🧪 Test Results

DataQA has been validated against multiple real-world datasets with varying complexity:

### Test Dataset Results

| Dataset | Rows | Issues Found | Risk Score | Status | Time |
|---------|------|--------------|------------|--------|------|
| **Amazon Laptops** (Original) | 209 | 15 | 66/100 | 🟡 HIGH | <1s |
| **Amazon Laptops** (Corrupted v2) | 232 | 18 | **97/100** | 🔴 **CRITICAL** | <1s |
| **Indian Toy Sales** (Original) | 100,000 | 12 | 40/100 | 🟢 MEDIUM | ~3s |
| **Indian Toy Sales** (Corrupted) | 100,030 | 19 | **79/100** | 🔴 **CRITICAL** | ~3s |

### Detection Capabilities

DataQA successfully detects:
- ✅ Missing values (30%+ missing data detection)
- ✅ Invalid data types (text in numeric fields)
- ✅ Extreme outliers (ratings: 100, -10, 999)
- ✅ Duplicate records (up to 20% duplication rate)
- ✅ Format inconsistencies ("8GB" vs "8 gb" vs "EIGHT GB")
- ✅ Null string variations ("NULL", "N/A", "none", "...")
- ✅ Negative values in price/quantity fields
- ✅ Whitespace and encoding issues

### Sample Datasets

Sample datasets are included in `tests/data/` to try out DataQA:

| Dataset | Size | Description | Use Case |
|---------|------|-------------|----------|
| Amazon Laptops (Original) | 209 rows | Web-scraped laptop data | Testing basic validation |
| Amazon Laptops (Corrupted) | 232 rows | Heavily corrupted version | Stress testing detection |
| Indian Toy Sales | 100K+ rows | Large retail dataset | Performance testing |

---

## Customizing Rules

Want to change what gets checked? Edit `config/rules.json`:

```json
{
  "required_columns": ["id", "name", "email"],
  "thresholds": {
    "missing_percent_high": 30,
    "outlier_std_dev": 3
  }
}
```

This lets you:
- Specify which columns must exist
- Set your own thresholds for problems
- Adjust severity levels

---

## 📸 Taking Screenshots

For README or LinkedIn posts, capture these key views:

1. **Hero Shot** - Full dashboard with risk assessment (use corrupted data for impact!)
2. **Risk Gauge** - Close-up of 97/100 CRITICAL score
3. **Interactive Charts** - All three visualizations together
4. **Detailed Table** - Color-coded issues with export button
5. **Before/After** - Side-by-side comparison of risk scores

**Pro Tip**: Use corrupted datasets (score 79-97) for more dramatic screenshots! 🎯

---

## 🚀 Use Cases

- **Data Scientists** - Validate datasets before modeling
- **Analysts** - Check data quality before creating dashboards
- **Data Engineers** - Monitor data pipeline quality
- **Students** - Learn data quality best practices
- **Researchers** - Ensure research data integrity

---

## 🛠️ Tech Stack

Built with modern Python tools:
- **[Streamlit](https://streamlit.io/)** - Interactive web interface
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[Plotly](https://plotly.com/)** - Interactive visualizations
- **[Matplotlib](https://matplotlib.org/)** & **[Seaborn](https://seaborn.pydata.org/)** - Statistical charts
- **[NumPy](https://numpy.org/)** - Numerical computing

---

## 🤝 Contributing

Found a bug or have a feature idea? Feel free to:
1. Open an issue
2. Submit a pull request
3. Reach out with suggestions

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

Built by **[Your Name]**
- LinkedIn: [Your Profile]
- GitHub: [Your GitHub]
- Email: [Your Email]

---

**Version 1.0** • Updated February 2026

*DataQA - Because clean data leads to better decisions.* 🎯
