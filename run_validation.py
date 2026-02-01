#!/usr/bin/env python3
"""
Main script to run complete data validation pipeline
Simple and easy to use!
"""

import sys
import io
from pathlib import Path
from src.data_loader import DataLoader
from src.validators import DataValidator
from src.risk_engine import RiskEngine
from src.report_generator import ReportGenerator

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def run_validation(file_path: str, file_type: str = 'csv', output_dir: str = 'outputs'):
    """
    Run complete validation pipeline
    
    Args:
        file_path: Path to your data file
        file_type: 'csv', 'excel', or 'sql'
        output_dir: Where to save reports
    """
    print("\n" + "="*60)
    print("     🚀 DATA VALIDATION PIPELINE")
    print("="*60 + "\n")
    
    # Step 1: Load data
    print("📂 Step 1: Loading data...")
    loader = DataLoader(file_path, source_type=file_type)
    df = loader.load()
    
    # Show basic info
    info = loader.get_info()
    print(f"   Loaded {info['rows']:,} rows and {info['columns']} columns")
    
    # Step 2: Run validations
    print("\n🔍 Step 2: Running validations...")
    validator = DataValidator(df)
    issues = validator.run_all_validations()
    
    # Step 3: Calculate risk
    print("\n⚠️  Step 3: Calculating risk score...")
    risk_engine = RiskEngine()
    risk_score = risk_engine.calculate_risk(issues, df)
    
    print(f"   Risk Level: {risk_score.risk_level}")
    print(f"   Risk Score: {risk_score.total_score}/100")
    
    # Step 4: Generate reports
    print("\n📊 Step 4: Generating reports...")
    reporter = ReportGenerator(df, issues, risk_score)
    reporter.generate_all_reports(output_dir=output_dir)
    
    # Also export risk summary
    risk_engine.export_risk_summary(risk_score, issues, f"{output_dir}/risk_summary.txt")
    
    # Final summary
    print("\n" + "="*60)
    print("✅ VALIDATION COMPLETE!")
    print("="*60)
    print(f"\n📁 Reports saved to: {output_dir}/")
    print(f"   - validation_report.csv")
    print(f"   - validation_report.xlsx")
    print(f"   - validation_report.html")
    print(f"   - interactive_dashboard.html  ⭐ NEW!")
    print(f"   - risk_summary.txt")
    print("\n💡 Open interactive_dashboard.html in your browser for the best experience!")
    print("   Perfect for sharing on LinkedIn! 🚀\n")
    
    return df, issues, risk_score


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        # Use command line argument
        file_path = sys.argv[1]
        file_type = sys.argv[2] if len(sys.argv) > 2 else 'csv'
    else:
        # Default example
        print("Usage: python run_validation.py <file_path> [file_type]")
        print("\nExample:")
        print("  python run_validation.py data.csv csv")
        print("  python run_validation.py data.xlsx excel")
        print("\nRunning with sample data...\n")
        
        # Look for sample CSV file
        sample_files = list(Path('.').glob('*.csv'))
        if sample_files:
            file_path = str(sample_files[0])
            file_type = 'csv'
        else:
            print("❌ No CSV files found in current directory.")
            print("   Please provide a file path as argument.")
            sys.exit(1)
    
    # Run the validation
    run_validation(file_path, file_type)
