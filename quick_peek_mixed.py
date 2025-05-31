#!/usr/bin/env python3
"""
Quick peek at the mixed dataset structure
"""
import csv
from pathlib import Path

def peek_dataset(csv_path):
    """Show first few rows of a dataset."""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = []
            for i, row in enumerate(reader):
                lines.append(row)
                if i >= 5:  # First 6 rows (header + 5 data)
                    break
        
        print(f"📊 {csv_path.name} structure:")
        for i, line in enumerate(lines):
            print(f"  Row {i}: {line}")
        
        # Count total rows
        with open(csv_path, 'r', encoding='utf-8') as f:
            total_rows = sum(1 for line in f) - 1  # Subtract header
        print(f"  Total data rows: {total_rows}")
        
    except Exception as e:
        print(f"❌ Error reading {csv_path}: {e}")

if __name__ == "__main__":
    data_dir = Path("data")
    
    # Check mixed_contradictions.csv
    mixed_file = data_dir / "mixed_contradictions.csv"
    if mixed_file.exists():
        peek_dataset(mixed_file)
    else:
        print("❌ mixed_contradictions.csv not found")
        
    # Also check mixed_quick.csv
    quick_file = data_dir / "mixed_quick.csv"
    if quick_file.exists():
        print("\n" + "="*50)
        peek_dataset(quick_file)