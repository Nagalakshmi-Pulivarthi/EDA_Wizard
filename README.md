# DataQA - Data Quality Checker

A simple Python tool I built to check if my datasets have problems before analyzing them.

## What It Does

Checks your data for common issues:
- Missing values
- Duplicate records
- Wrong data types
- Date format problems
- Statistical outliers
- Unnamed columns

Then gives you a risk score (0-100) so you know if the data is safe to use.

## Screenshots

![Dashboard](screenshots/Dashboard_screeshot.png)

![Charts](screenshots/IssuesAnalysi_screenshot.png)

![Details](screenshots/Detailed_table_screenshot.png)

## How to Use

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the app:**
```bash
streamlit run app.py
```

Then upload your CSV or Excel file and see the results!

## What You Get

- Risk score and severity levels
- Interactive charts
- Detailed list of all issues
- Export reports (HTML format)

## Test Results

I tested it on real Kaggle datasets:

| Dataset | Rows | Issues | Risk Score |
|---------|------|--------|------------|
| Amazon Laptops | 209 | 15 | 66/100 🟡 |
| Corrupted Version | 232 | 18 | 97/100 🔴 |
| Toy Sales | 100,000 | 12 | 40/100 🟢 |
| Corrupted Version | 100,030 | 19 | 79/100 🔴 |

Works fast even on large datasets!

## Built With

- Python 3.13
- Streamlit (web interface)
- Pandas (data processing)
- Plotly (interactive charts)

---

Made with ☕ by someone who was tired of dealing with messy data
