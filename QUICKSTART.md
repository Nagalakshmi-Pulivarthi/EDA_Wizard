# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
python demo.py
```

This will create sample data, run validations, and generate all reports!

### 3. Try with Your Own Data
```bash
python run_validation.py your_data.csv
```

---

## 📖 Common Use Cases

### Use Case 1: Basic Validation
**Goal**: Check if your CSV file has any quality issues

```bash
python run_validation.py sales_data.csv
```

**Output**: 4 reports in `outputs/` folder

---

### Use Case 2: Excel Validation
**Goal**: Validate an Excel file

```bash
python run_validation.py customer_data.xlsx excel
```

---

### Use Case 3: Custom Python Script
**Goal**: Run specific validations programmatically

```python
from src import DataLoader, DataValidator

# Load data
loader = DataLoader("data.csv", source_type="csv")
df = loader.load()

# Run validations
validator = DataValidator(df)

# Run all checks
issues = validator.run_all_validations()

# Or run specific checks
validator.check_missing_values_column()
validator.check_duplicates(key_columns=['id', 'email'])
validator.check_value_ranges({'age': {'min': 0, 'max': 120}})

# Get issues
for issue in validator.issues:
    print(f"[{issue.severity}] {issue.message}")
```

---

### Use Case 4: Streamlit Interactive EDA
**Goal**: Visual data exploration

```bash
streamlit run app.py
```

Then upload your file and explore!

---

## 🎯 What Each Module Does

| Module | Purpose | When to Use |
|--------|---------|-------------|
| `data_loader.py` | Load CSV/Excel/SQL | Need to load data from various sources |
| `validators.py` | Run 8 validation checks | Need detailed data quality checks |
| `risk_engine.py` | Calculate risk score | Need overall quality assessment |
| `report_generator.py` | Create reports | Need formatted output |
| `run_validation.py` | All-in-one pipeline | Quick command-line validation |
| `app.py` | Streamlit web app | Visual exploration & charts |
| `main.py` | Classic EDA class | Programmatic EDA |

---

## 🔧 Configuration

### Customize Validation Rules
Edit `config/rules.json`:

```json
{
  "thresholds": {
    "missing_percent_high": 30,    // > 30% missing = HIGH severity
    "missing_percent_medium": 10,   // > 10% missing = MEDIUM severity
    "outlier_std_dev": 3            // Beyond 3 std devs = outlier
  },
  "required_columns": ["id", "name", "email"],
  "critical_columns": ["id"]
}
```

---

## 📊 Understanding the Reports

### 1. CSV Report (`validation_report.csv`)
- Simple spreadsheet format
- One row per issue
- Easy to share and filter

### 2. Excel Report (`validation_report.xlsx`)
- Multi-sheet workbook
- Summary, Issues, Data Overview, Recommendations
- Best for comprehensive review

### 3. HTML Report (`validation_report.html`)
- Beautiful visual report
- Color-coded issues
- Open in browser
- Best for presentations

### 4. Risk Summary (`risk_summary.txt`)
- Text format
- Overall assessment
- Actionable recommendations
- Good for documentation

---

## 💡 Tips & Best Practices

### ✅ DO:
- Run validation BEFORE analyzing data
- Check the HTML report first (easiest to read)
- Address HIGH severity issues immediately
- Customize thresholds in `config/rules.json`
- Use Streamlit for visual exploration after validation

### ❌ DON'T:
- Use data with HIGH risk score for critical decisions
- Ignore MEDIUM severity issues
- Skip validation on production data
- Forget to check the recommendations

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Problem: "Config file not found"
**Solution**: Create `config/rules.json` or code will use defaults

### Problem: "outputs folder not found"
**Solution**: Folder is created automatically on first run

### Problem: Import errors in src/
**Solution**: Make sure you're running from project root directory

---

## 🎓 Learning Path

1. **Beginner**: Run `demo.py` to see it in action
2. **Intermediate**: Use `run_validation.py` with your data
3. **Advanced**: Import modules in your own scripts
4. **Expert**: Customize validators and add new checks

---

## 📞 Need Help?

1. Check this guide
2. Look at `demo.py` for examples
3. Read the main `README.md`
4. Check code comments in `src/` modules

---

## 🎯 Next Steps

After validation, you can:
1. Fix issues manually
2. Use Streamlit app for visual analysis
3. Export cleaned data
4. Generate EDA reports
5. Share validation reports with team

Happy validating! 🚀
