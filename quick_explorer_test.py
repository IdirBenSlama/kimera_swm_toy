#!/usr/bin/env python3
"""
Quick test of explorer functionality
"""

def test_explorer():
    """Test explorer.html can be read and has echo support"""
    try:
        with open("tools/explorer.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"✅ Explorer file read successfully ({len(content)} chars)")
        
        # Check for echo support
        checks = [
            ("echo1 support", "echo1" in content.lower()),
            ("echo2 support", "echo2" in content.lower()),
            ("echo-cell styling", "echo-cell" in content)
        ]
        
        all_passed = True
        for name, result in checks:
            status = "✅" if result else "❌"
            print(f"{status} {name}: {result}")
            if not result:
                all_passed = False
        
        if all_passed:
            print("🎉 Explorer has all required echo support!")
        else:
            print("❌ Explorer missing some echo features")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing explorer: {e}")
        return False

if __name__ == "__main__":
    test_explorer()