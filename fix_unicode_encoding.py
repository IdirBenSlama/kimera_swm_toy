#!/usr/bin/env python3
"""
Fix Unicode Encoding Issues in Test Suite
=========================================

This script replaces all emoji characters in test suite files with ASCII equivalents
to fix UnicodeEncodeError on Windows systems with cp1252 encoding.
"""

import os
import re
from pathlib import Path

# Emoji to ASCII mapping
EMOJI_MAP = {
    "🚀": "[RUN]",
    "✅": "[OK]", 
    "❌": "[FAIL]",
    "🎯": "[TARGET]",
    "🔍": "[CHECK]",
    "🧪": "[TEST]",
    "📊": "[SUMMARY]",
    "🏁": "[END]",
    "⏭️": "[SKIP]",
    "🔧": "[TOOL]",
    "⚙️": "[CONFIG]",
    "📁": "[FILES]",
    "⚠️": "[WARN]",
    "💥": "[ERROR]",
    "⏰": "[TIME]",
    "🎉": "[SUCCESS]",
    "📚": "[DOCS]",
    "🛑": "[STOP]",
    "🚑": "[FIX]",
    "⚡": "[FAST]",
    "🧠": "[THINK]",
    "🚩": "[FLAG]",
    "🔎": "[SEARCH]",
    "🎪": "[DEMO]",
    "🌟": "[STAR]",
    "💡": "[IDEA]",
    "🔥": "[HOT]",
    "⭐": "[STAR]",
    "🎊": "[PARTY]",
    "🎈": "[BALLOON]",
    "🎁": "[GIFT]",
    "🎂": "[CAKE]",
    "🎵": "[MUSIC]",
    "🎶": "[NOTE]",
    "🎸": "[GUITAR]",
    "🎤": "[MIC]",
    "🎧": "[HEADPHONE]",
    "🎬": "[MOVIE]",
    "🎭": "[THEATER]",
    "🎨": "[ART]",
    "🎯": "[DART]",
    "🎲": "[DICE]",
    "🎮": "[GAME]",
    "🎰": "[SLOT]",
    "🎳": "[BOWLING]",
    "🎺": "[TRUMPET]",
    "🎻": "[VIOLIN]",
    "🎼": "[SCORE]",
    "🎽": "[SHIRT]",
    "🎾": "[TENNIS]",
    "🎿": "[SKI]",
    "🏀": "[BASKETBALL]",
    "🏁": "[FINISH]",
    "🏂": "[SNOWBOARD]",
    "🏃": "[RUN]",
    "🏄": "[SURF]",
    "🏅": "[MEDAL]",
    "🏆": "[TROPHY]",
    "🏇": "[HORSE]",
    "🏈": "[FOOTBALL]",
    "🏉": "[RUGBY]",
    "🏊": "[SWIM]",
    "🏋": "[LIFT]",
    "🏌": "[GOLF]",
    "🏍": "[BIKE]",
    "🏎": "[RACE]",
    "🏏": "[CRICKET]",
    "🏐": "[VOLLEYBALL]",
    "🏑": "[HOCKEY]",
    "🏒": "[ICE_HOCKEY]",
    "🏓": "[PING_PONG]",
    "🏔": "[MOUNTAIN]",
    "🏕": "[CAMP]",
    "🏖": "[BEACH]",
    "🏗": "[CONSTRUCTION]",
    "🏘": "[HOUSES]",
    "🏙": "[CITY]",
    "🏚": "[HOUSE]",
    "🏛": "[BUILDING]",
    "🏜": "[DESERT]",
    "🏝": "[ISLAND]",
    "🏞": "[PARK]",
    "🏟": "[STADIUM]",
    "🏠": "[HOME]",
    "🏡": "[HOUSE_GARDEN]",
    "🏢": "[OFFICE]",
    "🏣": "[POST]",
    "🏤": "[EURO_POST]",
    "🏥": "[HOSPITAL]",
    "🏦": "[BANK]",
    "🏧": "[ATM]",
    "🏨": "[HOTEL]",
    "🏩": "[LOVE_HOTEL]",
    "🏪": "[STORE]",
    "🏫": "[SCHOOL]",
    "🏬": "[DEPARTMENT]",
    "🏭": "[FACTORY]",
    "🏮": "[LANTERN]",
    "🏯": "[CASTLE]",
    "🏰": "[CASTLE_EUROPEAN]",
}

def replace_emoji_in_text(text):
    """Replace emoji characters with ASCII equivalents."""
    for emoji, ascii_replacement in EMOJI_MAP.items():
        text = text.replace(emoji, ascii_replacement)
    return text

def fix_file(file_path):
    """Fix emoji characters in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = replace_emoji_in_text(content)
        
        if original_content != fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix emoji characters in all test suite files."""
    print("[FIX] Unicode Encoding Fix for Test Suite")
    print("=" * 50)
    
    # Files to fix (test suite and related files)
    files_to_fix = [
        "test_suite.py",
        "run_test_suite.py", 
        "test_config.py",
        "setup_tests.py",
        "quick_test_validation.py",
        "test_suite_demo.py",
        "TEST_SUITE_README.md",
        "TEST_SUITE_IMPLEMENTATION_SUMMARY.md"
    ]
    
    # Also find any other test files that might have emoji
    for file_pattern in ["test_*.py", "run_*.py", "*_test.py"]:
        for file_path in Path(".").glob(file_pattern):
            if file_path.name not in files_to_fix:
                files_to_fix.append(str(file_path))
    
    fixed_count = 0
    total_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            total_count += 1
            print(f"[CHECK] {file_path}...", end=" ")
            
            if fix_file(file_path):
                print("[FIXED]")
                fixed_count += 1
            else:
                print("[OK]")
        else:
            print(f"[SKIP] {file_path} (not found)")
    
    print("\n" + "=" * 50)
    print(f"[SUMMARY] Fixed {fixed_count}/{total_count} files")
    
    if fixed_count > 0:
        print("\n[SUCCESS] Unicode encoding issues fixed!")
        print("You can now run the test suite without UnicodeEncodeError.")
        print("\nTry running:")
        print("  python run_test_suite.py --mode quick")
        print("  python test_suite_demo.py")
    else:
        print("\n[OK] No emoji characters found in test files.")
    
    return 0

if __name__ == "__main__":
    exit(main())