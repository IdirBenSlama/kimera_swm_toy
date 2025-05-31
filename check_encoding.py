#!/usr/bin/env python3
"""
Check for encoding issues in explorer.html
"""
import sys
import subprocess

def check_file_encoding(filepath):
    """Check for problematic characters in a file"""
    try:
        # Try reading as UTF-8 first
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ {filepath} reads fine as UTF-8")
        
        # Check for any non-ASCII characters
        non_ascii_chars = []
        for i, char in enumerate(content):
            if ord(char) > 127:
                non_ascii_chars.append((i, char, ord(char), hex(ord(char))))
        
        if non_ascii_chars:
            print(f"⚠️  Found {len(non_ascii_chars)} non-ASCII characters:")
            for pos, char, code, hex_code in non_ascii_chars[:10]:  # Show first 10
                line_num = content[:pos].count('\n') + 1
                print(f"  Line {line_num}, pos {pos}: '{char}' (U+{hex_code[2:].upper().zfill(4)}, {code})")
            return False
        else:
            print("✅ All characters are ASCII")
            return True
            
    except UnicodeDecodeError as e:
        print(f"❌ UTF-8 decode error: {e}")
        
        # Try reading as CP-1252
        try:
            with open(filepath, 'r', encoding='cp1252') as f:
                content = f.read()
            print(f"⚠️  File reads as CP-1252, converting to UTF-8...")
            
            # Write back as UTF-8
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Converted {filepath} to UTF-8")
            return True
            
        except Exception as e2:
            print(f"❌ CP-1252 read also failed: {e2}")
            return False
    
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

if __name__ == "__main__":
    filepath = "tools/explorer.html"
    success = check_file_encoding(filepath)
    sys.exit(0 if success else 1)