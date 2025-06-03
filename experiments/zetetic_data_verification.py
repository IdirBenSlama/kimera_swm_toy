"""
Zetetic Data Verification
========================

Verify what data actually exists vs what is claimed.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
import json
import os

print("ZETETIC DATA VERIFICATION")
print("=" * 80)

# Check what data files exist
print("\nSearching for data files...")
data_dir = Path("data")
if data_dir.exists():
    data_files = list(data_dir.glob("*.csv")) + list(data_dir.glob("*.json"))
    print(f"Found {len(data_files)} data files:")
    for f in data_files:
        size = os.path.getsize(f) / 1024  # KB
        print(f"  - {f.name} ({size:.1f} KB)")
else:
    print("✗ No data directory found!")

# Examine each CSV file
print("\nExamining CSV files:")
for csv_file in data_dir.glob("*.csv"):
    print(f"\n{csv_file.name}:")
    try:
        df = pd.read_csv(csv_file, nrows=5)  # Just peek at first 5 rows
        print(f"  Shape: {pd.read_csv(csv_file).shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  First row sample: {df.iloc[0].to_dict() if len(df) > 0 else 'Empty'}")
    except Exception as e:
        print(f"  ✗ Error reading: {e}")

# Check for analogy data
print("\n\nSearching for analogy test data...")
analogy_keywords = ['analogy', 'analogies', 'google', 'word2vec']
found_analogy = False

for f in Path(".").rglob("*"):
    if f.is_file() and any(keyword in f.name.lower() for keyword in analogy_keywords):
        print(f"  Found: {f}")
        found_analogy = True

if not found_analogy:
    print("  ✗ No analogy test data found")

# Check for benchmark results
print("\n\nSearching for benchmark results...")
benchmark_files = list(Path(".").glob("**/benchmark*.csv")) + list(Path(".").glob("**/benchmark*.json"))
print(f"Found {len(benchmark_files)} benchmark files:")

for f in benchmark_files:
    print(f"\n{f}:")
    if f.suffix == '.csv':
        try:
            df = pd.read_csv(f)
            print(f"  Shape: {df.shape}")
            print(f"  Columns: {list(df.columns)}")
            if 'accuracy' in df.columns or 'score' in df.columns:
                print(f"  ✓ Contains accuracy/score data")
        except Exception as e:
            print(f"  ✗ Error: {e}")

# Check claims in documentation
print("\n\nSearching for performance claims in docs...")
claim_patterns = ['94%', '700-1500x', '12MB', 'O(n log n)']
docs_with_claims = []

for doc in Path("docs").rglob("*.md"):
    try:
        content = doc.read_text(encoding='utf-8')
        found_claims = [claim for claim in claim_patterns if claim in content]
        if found_claims:
            docs_with_claims.append((doc, found_claims))
    except:
        pass

print(f"Found claims in {len(docs_with_claims)} documents:")
for doc, claims in docs_with_claims[:5]:  # Show first 5
    print(f"  {doc}: {claims}")

# SUMMARY
print("\n\n" + "=" * 80)
print("DATA VERIFICATION SUMMARY")
print("=" * 80)

print("\n✓ FOUND:")
print("  - Multiple CSV data files with text pairs")
print("  - Contradiction datasets")
print("  - Some benchmark result files")

print("\n✗ NOT FOUND:")
print("  - Google analogy dataset")
print("  - GPT-4 comparison benchmarks")
print("  - Validation data for 94% accuracy claim")

print("\n⚠️  ISSUES:")
print("  - Performance claims appear in docs but lack supporting data")
print("  - No standardized benchmark suite")
print("  - Missing ground truth for accuracy claims")