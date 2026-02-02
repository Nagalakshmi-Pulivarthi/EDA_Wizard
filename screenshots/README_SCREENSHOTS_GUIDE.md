# 📸 Screenshot Guide for DataQA

This folder should contain the following screenshots for the main README.md file.

## Required Screenshots

### 1. `dashboard_full.png` ⭐ PRIORITY
**What to capture:**
- Upload the **corrupted Amazon Laptops** dataset (97/100 CRITICAL score)
- Show the full view including:
  - Dataset Overview (rows, columns, duplicates, risk level)
  - Risk Assessment section with 3 metrics
  - Risk Score: 97/100
  - Total Issues: 18
  - High Severity count

**How to take it:**
1. Open app.py in Streamlit
2. Upload: `tests/data/amazon_laptops - corrupted_v2.csv`
3. Wait for it to load completely
4. Screenshot from "Dataset Overview" to "Risk Assessment" section

---

### 2. `charts_overview.png` ⭐ PRIORITY
**What to capture:**
- The three interactive charts in the "Interactive Data Quality Dashboard" section:
  1. Issues by Severity (bar chart with HIGH annotation)
  2. Issues by Column (purple bar chart)
  3. Issues by Type (donut/pie chart)

**How to take it:**
1. Scroll to "Interactive Data Quality Dashboard"
2. Make sure all 3 charts are visible in one screenshot
3. Switch to "Issues Analysis" tab if needed
4. Screenshot the entire chart section

---

### 3. `detailed_table.png`
**What to capture:**
- The "Detailed Table" tab showing:
  - Color-coded severity rows (red, yellow, blue backgrounds)
  - All columns: Severity, Type, Message, Column, Affected Rows
  - "Download Issues as CSV" button

**How to take it:**
1. Click on "Detailed Table" tab
2. Make sure table is fully visible
3. Screenshot showing at least 10-15 rows with color coding

---

### 4. `risk_gauge_closeup.png` (Optional but Impressive)
**What to capture:**
- Close-up of the Risk Score gauge showing 97/100 in the red zone

**How to take it:**
1. Zoom in on the gauge chart
2. Make sure the needle is clearly visible pointing to 97
3. Show the color gradient (green -> yellow -> red)

---

### 5. `before_after_comparison.png` (Optional - Create Manually)
**What to create:**
- Side-by-side comparison image showing:
  - LEFT: Original data risk score (66 HIGH)
  - RIGHT: Corrupted data risk score (97 CRITICAL)

**How to create it:**
1. Take screenshot of gauge with original data
2. Take screenshot of gauge with corrupted data
3. Use an image editor to place them side-by-side
4. Add labels: "Before" and "After"

---

## Pro Tips for Great Screenshots

### Browser Setup
- ✅ Use Chrome or Edge (clean UI)
- ✅ Press F11 for full screen (hides browser chrome)
- ✅ Use 100% zoom level (Ctrl+0)
- ✅ Hide bookmarks bar (Ctrl+Shift+B)

### Screenshot Tools
- **Windows**: `Win + Shift + S` (Snipping Tool)
- **macOS**: `Cmd + Shift + 4`
- **Browser Extension**: Fireshot, Awesome Screenshot

### Image Quality
- Save as PNG (not JPG) for better quality
- Crop out unnecessary white space
- Keep dimensions reasonable: 1200-1600px width
- Compress if file size > 500KB

---

## Current Status

Place checkmarks when screenshots are complete:

- [ ] dashboard_full.png
- [ ] charts_overview.png
- [ ] detailed_table.png
- [ ] risk_gauge_closeup.png
- [ ] before_after_comparison.png

---

## For LinkedIn Posts

**Best screenshots for social media:**
1. `dashboard_full.png` - Shows the complete tool (BEST for single post)
2. `charts_overview.png` - Eye-catching visualizations
3. Create a carousel with all screenshots for maximum engagement

---

**Note**: Update README.md image paths after adding screenshots:
```markdown
![Dashboard Preview](screenshots/dashboard_full.png)
```
