#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

# Test the specific unit test that was failing
try:
    print("Running test_echoform_core.py...")
    exec(open('tests/unit/test_echoform_core.py').read())
except Exception as e:
    print(f"❌ test_echoform_core.py failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nRunning test_identity.py...")
    exec(open('tests/unit/test_identity.py').read())
except Exception as e:
    print(f"❌ test_identity.py failed: {e}")
    import traceback
    traceback.print_exc()