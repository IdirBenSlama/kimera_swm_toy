#!/usr/bin/env python3
"""
Simple test to isolate the explorer issue
"""

def test_explorer_simple():
    """Simple explorer test"""
    try:
        print("Testing explorer.html...")
        
        # Try to read the file
        with open("tools/explorer.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"✅ Read {len(content)} characters successfully")
        
        # Check for required content
        checks = [
            ("echo1", "echo1" in content.lower()),
            ("echo2", "echo2" in content.lower()),
            ("echo-cell", "echo-cell" in content)
        ]
        
        for name, result in checks:
            print(f"{'✅' if result else '❌'} {name}: {result}")
        
        return all(result for _, result in checks)
        
    except UnicodeDecodeError as e:
        print(f"❌ Unicode decode error: {e}")
        print(f"Position: {e.start}-{e.end}")
        
        # Show the problematic bytes
        with open("tools/explorer.html", "rb") as f:
            data = f.read()
        
        problem_bytes = data[e.start:e.end]
        print(f"Problematic bytes: {[hex(b) for b in problem_bytes]}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_explorer_simple()