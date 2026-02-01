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

✅ **Risk Score** - A simple 0-100 score (lower is better)  
✅ **Quality Issues** - Clear list of what's wrong  
✅ **Recommendations** - What to fix first  
✅ **Visual Reports** - Easy-to-read charts and tables  

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

- **0-24 = LOW** 🟢 Your data is good to go
- **25-49 = MEDIUM** 🟡 Some issues to fix, but usable
- **50-74 = HIGH** 🟠 Serious problems - fix before analyzing
- **75-100 = CRITICAL** 🔴 Too many issues - don't use this data yet

---

## What You Get

DataQA generates several reports for you:

### 1. Web Dashboard
- Interactive charts
- Color-coded issues
- One-click downloads

### 2. Excel Report
- Summary sheet with your score
- Detailed issues list
- Column-by-column breakdown
- Recommendations

### 3. HTML Report
- Beautiful styled report
- Easy to share with your team
- Opens in any browser

### 4. CSV Files
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

## Common Questions

**Q: Do I need to know Python?**  
A: Nope! Just run the web app and upload your file.

**Q: What file formats work?**  
A: CSV and Excel (.xlsx) files.

**Q: Can I check multiple files?**  
A: Currently one at a time. Multi-file support coming soon!

**Q: Is my data safe?**  
A: Yes! Everything runs on your computer. Nothing is uploaded anywhere.

**Q: How big can my data be?**  
A: Tested with files up to 1 million rows. Larger files may be slower.

**Q: What's the difference between severity and risk score?**  
A: Severity (HIGH/MEDIUM/LOW) describes each individual issue. Risk score (0-100) is your overall data quality.

---

## Troubleshooting

**Problem: "streamlit: command not found"**  
→ Make sure you installed everything: `pip install -r requirements.txt`

**Problem: "ModuleNotFoundError"**  
→ You're missing a package. Run: `pip install -r requirements.txt`

**Problem: My file won't upload**  
→ Make sure it's a .csv or .xlsx file and not corrupted

**Problem: The app is slow**  
→ Large files take longer. Try with a smaller sample first.

---

## What's Next?

DataQA is actively being improved. Coming soon:
- 📁 Multi-file comparison
- 🗄️ Direct database connections
- 📊 Advanced visualizations
- 🤖 Auto-fix suggestions
- 📧 Email alerts

---

## Need Help?

Found a bug? Have a suggestion? Want to contribute?  
Open an issue on GitHub or reach out!

---

## Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web interface
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) - Charts

---

**Version 1.0** • Updated January 2026

*DataQA - Because clean data leads to better decisions.*
