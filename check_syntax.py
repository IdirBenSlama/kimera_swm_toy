#!/usr/bin/env python3
import ast
import sys

def check_syntax(filename):
    try:
        with open(filename, 'r') as f:
            source = f.read()
        ast.parse(source)
        print(f"✅ {filename} - syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {filename} - syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ {filename} - error: {e}")
        return False

files_to_check = [
    'src/kimera/echoform.py',
    'src/kimera/identity.py', 
    'src/kimera/storage.py'
]

all_good = True
for filename in files_to_check:
    if not check_syntax(filename):
        all_good = False

if all_good:
    print("\n🎉 All files have valid syntax!")
else:
    print("\n❌ Some files have syntax errors")
    sys.exit(1)