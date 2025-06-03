"""
Fix False Claims in Documentation
=================================

This script updates all documentation to remove false performance claims.
"""
import re
from pathlib import Path

# Define replacements
REPLACEMENTS = [
    # False performance claims
    (r"700-1500x faster than GPT-4[^\n]*", 
     "Efficient resonance calculation (~3,000 pairs/second)"),
    
    (r"700-1500x speedup[^\n]*",
     "Efficient processing (no external benchmarks available)"),
    
    # False accuracy claims
    (r"94% accuracy on analogy tasks[^\n]*",
     "No standardized benchmarks available"),
     
    (r"exceeding human performance[^\n]*",
     "Performance varies by task"),
    
    # False memory claims
    (r"12MB for 1M concepts[^\n]*",
     "~1.5 GB for 1M concepts"),
     
    (r"100x less memory[^\n]*",
     "Memory usage: ~1.5 MB per 1,000 texts"),
    
    # False complexity claims
    (r"O\(n log n\) complexity for core operations",
     "O(n²) complexity for pairwise operations"),
     
    (r"O\(n log n\) scalability",
     "O(n²) scaling for resonance calculations"),
]

def fix_file(filepath):
    """Fix false claims in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        for pattern, replacement in REPLACEMENTS:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes.extend(matches)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n✓ Fixed {filepath.name}:")
            for change in changes[:3]:  # Show first 3 changes
                print(f"  - Removed: '{change[:60]}...'")
            if len(changes) > 3:
                print(f"  - And {len(changes)-3} more...")
            return True
        return False
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Fix false claims in all documentation."""
    print("Fixing False Claims in Documentation")
    print("=" * 60)
    
    # Find all markdown files
    docs_path = Path("docs")
    md_files = list(docs_path.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files")
    
    fixed_count = 0
    for filepath in md_files:
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"Summary: Fixed {fixed_count} files")
    
    # Also check root README
    if Path("README.md").exists():
        print("\nChecking root README.md...")
        if fix_file(Path("README.md")):
            print("✓ Root README.md already updated")
        else:
            print("✓ Root README.md clean")

if __name__ == "__main__":
    main()