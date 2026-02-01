# DataQA - Your Data Quality Assistant

**Make sure your data is ready before you analyze it.**

DataQA is a simple Python tool that checks your data for common problems - missing values, duplicates, formatting issues, and more. It gives you a clear quality score and tells you exactly what to fix.

---

## Why Use DataQA?

Ever loaded a dataset only to find:
- 😕 Half the values are missing?
- 😱 Duplicate records everywhere?
- 🤔 Dates in weird formats?
- 😤 "Unnamed" columns with no idea what they mean?

**DataQA catches these problems before they ruin your analysis.**

---

## What Does It Do?

DataQA checks your data and gives you:

**Risk Score** - A simple 0-100 score (lower is better)  
**Quality Issues** - Clear list of what's wrong  
**Recommendations** - What to fix first  
**Visual Reports** - Easy-to-read charts and tables  

Plus, you get basic stats and correlations to understand your data better.

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

## What Gets Checked?

DataQA looks for these common problems:

| Check | What It Does |
|-------|--------------|
| **Missing Values** | Finds blank cells in your data |
| **Duplicates** | Catches repeated rows |
| **Data Types** | Makes sure numbers are numbers, dates are dates, etc. |
| **Date Formats** | Finds invalid or inconsistent dates |
| **Outliers** | Spots values that seem way off |
| **Required Columns** | Checks if important columns exist |
| **Value Ranges** | Makes sure values are within expected limits |

---

## Understanding Your Risk Score

After checking your data, DataQA gives you a risk score:

- **0-24 = LOW** - Your data is good to go
- **25-49 = MEDIUM** - Some issues to fix, but usable
- **50-74 = HIGH** - Serious problems - fix before analyzing
- **75-100 = CRITICAL** - Too many issues - don't use this data yet

---

## What You Get

DataQA generates several reports for you:

### 1. Interactive Plotly Dashboard ⭐ NEW!
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
└── outputs/                 # Your reports go here
```

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

## Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web interface
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) - Charts

---

**Version 1.0** • Updated January 2026

*DataQA - Because clean data leads to better decisions.*
