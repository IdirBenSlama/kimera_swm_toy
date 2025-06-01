#!/usr/bin/env python3
import os

# Find all .md files in current directory
md_files = [f for f in os.listdir('.') if f.endswith('.md')]
print("Markdown files found:")
for f in sorted(md_files):
    print(f"  {f}")