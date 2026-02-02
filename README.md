# DataQA - Because Messy Data is a Problem We've All Had

I built this tool after spending way too many hours staring at datasets wondering "why are my results so weird?" only to discover the data was a mess. Sound familiar?

DataQA is a Python tool that checks your data for common problems before you waste time analyzing it. It gives you a simple score and tells you exactly what's broken.

---

## The Story Behind This

You know that moment when you've already built half your analysis, made some charts, maybe even showed them to someone... and then you realize your dataset had 30% missing values all along? Yeah, I've been there. Too many times.

So I built DataQA to catch these issues upfront. Upload your data, get a score in seconds, fix what's broken, then analyze with confidence.

---

## What It Actually Does

Here's what happens when you upload a file:

**The tool checks 8 common problems:**
- Missing values (the silent killer)
- Duplicate rows (why is everything doubled?)
- Wrong data types (why is "price" stored as text?)
- Weird date formats
- Outliers that don't make sense
- Columns that shouldn't be there
- Values that are out of reasonable ranges
- Those annoying "Unnamed" columns

**Then it gives you:**
- A risk score (0-100, where 0 is perfect)
- A color-coded severity level (green/yellow/orange/red)
- Interactive charts showing where the problems are
- A detailed list of every issue found
- Recommendations on what to fix first

---

## Real Example

I tested this on an Amazon laptops dataset. Here's what happened:

**Original data:** 209 rows, looked okay at first glance
- DataQA found 15 issues
- Risk score: 66/100 (HIGH risk)

**Then I deliberately corrupted it** to stress-test the tool:
- Added missing values, duplicates, invalid formats, etc.
- DataQA caught everything
- Risk score jumped to 97/100 (CRITICAL - don't touch this data!)

The tool successfully detected all the problems I introduced, plus a few I didn't even realize were there.

---

## Dashboard Preview

When you upload a file, you'll see something like this:

![Dashboard Preview](screenshots/dashboard_full.png)
*The main dashboard showing a risk score of 97/100 - this data needs serious cleanup*

![Interactive Charts](screenshots/charts_overview.png)
*Three interactive charts showing where the issues are concentrated*

![Detailed Table](screenshots/detailed_table.png)
*Every issue listed with color-coded severity levels*

### Real Test Example

Here's what happened when I tested it on real data:

| Dataset | Rows | Issues | Risk Score |
|---------|------|--------|------------|
| Amazon Laptops (clean-ish) | 209 | 15 | 66/100 |
| Same data, but corrupted | 232 | 18 | **97/100** |

The corrupted version had missing values, duplicates, invalid formats, and outliers. DataQA caught all of it.

---

## Getting Started

You'll need Python 3.13 or newer installed. Then:

```bash
# Clone this repo
cd EDA_Automation

# Install the dependencies
pip install -r requirements.txt

# Run it
streamlit run app.py
```

That's literally it. Your browser will open, drag in a CSV or Excel file, and you'll see your data quality score instantly.

---

## Using It

There are two ways to use DataQA:

### Option 1: The Web Interface (easier)

```bash
streamlit run app.py
```

Upload your file, click around the interactive charts, download reports. No coding needed.

### Option 2: Command Line (for automation)

```bash
python run_validation.py your_data.csv
```

This checks your data and saves all the reports to an `outputs/` folder. Great if you want to run this as part of an automated pipeline.

---

## Understanding the Risk Score

After checking your data, you get a score from 0-100:

- **0-24 (Green)** = Your data looks good, go ahead and analyze
- **25-49 (Yellow)** = Some issues but probably usable, review them first
- **50-74 (Orange)** = Significant problems, fix these before analyzing
- **75-100 (Red)** = Critical issues, don't analyze this data yet

The higher the score, the messier your data. Simple as that.

---

## What Gets Checked

The tool runs 8 different checks on your data:

1. **Missing Values** - How many blank cells do you have?
2. **Duplicates** - Any rows that are exactly the same?
3. **Data Types** - Is "price" actually stored as a number, or is it text?
4. **Date Formats** - Can the dates be parsed correctly?
5. **Outliers** - Any values that are suspiciously high or low?
6. **Required Columns** - Are the important columns present?
7. **Value Ranges** - Are values within reasonable limits? (no negative prices, ratings over 100, etc.)
8. **Unnamed Columns** - Those annoying "Unnamed: 0" columns

Each issue gets a severity rating (HIGH, MEDIUM, or LOW) based on how much it affects your data quality.

---

## What Reports Do You Get?

DataQA generates several different report formats:

1. **Interactive Web Dashboard** - The Streamlit interface with clickable charts
2. **Plotly Dashboard** - A standalone HTML file you can share with anyone (opens in any browser, no Python needed)
3. **Excel Report** - Summary sheet, detailed issues, column breakdowns, recommendations
4. **HTML Report** - Styled report for sharing with your team
5. **CSV Files** - Simple tables you can import into Excel or other tools

All reports are saved to the `outputs/` folder.

---

## Project Structure

```
EDA_Automation/
├── app.py                    # The web interface (run this)
├── run_validation.py         # Command-line version
├── requirements.txt          # Dependencies
├── config/
│   └── rules.json           # Validation rules (customize here)
├── src/                     # Core code
├── outputs/                 # Reports go here
└── tests/data/              # Sample datasets
```

---## Test Results

I tested DataQA on real datasets to see how well it catches problems:

| Dataset | Rows | Issues Found | Risk Score | Processing Time |
|---------|------|--------------|------------|----------------|
| Amazon Laptops (original) | 209 | 15 | 66/100 (HIGH) | < 1 second |
| Amazon Laptops (corrupted) | 232 | 18 | 97/100 (CRITICAL) | < 1 second |
| Indian Toy Sales | 100,000 | 12 | 40/100 (MEDIUM) | ~3 seconds |

The tool successfully caught everything I threw at it - missing values, duplicates, invalid data types, format issues, outliers, negative prices, and more.

Sample datasets are included in `tests/data/` if you want to try it yourself.

---

## Customizing It

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

This lets you specify which columns must exist and adjust the thresholds for what counts as a "problem."

---

## Who This Is For

- **Data scientists** who are tired of discovering data issues mid-analysis
- **Analysts** who need to validate data before building dashboards
- **Data engineers** who want to monitor pipeline quality
- **Students** learning about data quality best practices
- **Anyone** working with datasets and wanting to catch problems early

---

## Built With

- Python 3.13
- Streamlit (for the web interface)
- Pandas (for data analysis)
- Plotly (for interactive charts)
- Matplotlib & Seaborn (for visualizations)

---

## Future Ideas

Some things I'm thinking about adding:
- More validation checks (consistency rules, referential integrity, etc.)
- Support for databases (not just CSV/Excel)
- API endpoint for programmatic access
- Scheduled checks (run validation automatically on a schedule)

If you have ideas, let me know!

---

## License

MIT License - use it however you want.

---

*Built because I got tired of messy data breaking my analyses. Hope it helps you too.*

**Version 1.0** • February 2026
