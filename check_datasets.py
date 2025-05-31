#!/usr/bin/env python3
"""
Check available datasets and their structure
"""
import csv
from pathlib import Path

def analyze_dataset(csv_path):
    """Analyze a CSV dataset and show its structure."""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        print(f"\n📊 {csv_path.name}")
        print(f"   Rows: {len(rows)}")
        print(f"   Columns: {list(rows[0].keys()) if rows else 'None'}")
        
        # Check for label distribution if it's a mixed dataset
        if rows and 'label' in rows[0]:
            true_count = sum(1 for row in rows if row['label'].lower() in ['true', '1'])
            false_count = len(rows) - true_count
            print(f"   Labels: {true_count} True, {false_count} False ({true_count/len(rows):.1%} contradictory)")
        
        # Show sample row
        if rows:
            print(f"   Sample: {dict(list(rows[0].items())[:3])}")
            
    except Exception as e:
        print(f"   ❌ Error reading {csv_path.name}: {e}")

def main():
    print("🔍 Checking available datasets...")
    
    data_dir = Path("data")
    if not data_dir.exists():
        print("❌ No data/ directory found")
        return
    
    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        print("❌ No CSV files found in data/")
        return
    
    print(f"Found {len(csv_files)} datasets:")
    
    for csv_file in sorted(csv_files):
        analyze_dataset(csv_file)
    
    print(f"\n🎯 Recommended for mixed analysis:")
    for csv_file in csv_files:
        if "mixed" in csv_file.name.lower():
            print(f"   {csv_file}")

if __name__ == "__main__":
    main()