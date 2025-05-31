#!/usr/bin/env python3
"""
Test explorer encoding specifically
"""
import sys

def test_explorer_encoding():
    """Test explorer.html encoding"""
    try:
        # Try to read the file
        with open("tools/explorer.html", "r", encoding="utf-8") as f:
            content = f.read()
        print("✅ Explorer reads fine as UTF-8")
        
        # Check for echo support
        if "echo1" in content.lower():
            print("✅ Explorer has echo1 support")
        else:
            print("❌ Explorer missing echo1 support")
            
        if "echo2" in content.lower():
            print("✅ Explorer has echo2 support")
        else:
            print("❌ Explorer missing echo2 support")
            
        if "echo-cell" in content:
            print("✅ Explorer has echo-cell styling")
        else:
            print("❌ Explorer missing echo-cell styling")
            
        return True
        
    except UnicodeDecodeError as e:
        print(f"❌ UTF-8 decode error: {e}")
        print(f"Error at position: {e.start}-{e.end}")
        print(f"Problematic bytes: {e.object[e.start:e.end]}")
        
        # Try to read with different encodings
        for encoding in ['cp1252', 'latin1', 'iso-8859-1']:
            try:
                with open("tools/explorer.html", "r", encoding=encoding) as f:
                    content = f.read()
                print(f"✅ File reads with {encoding}")
                
                # Convert to UTF-8
                with open("tools/explorer.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Converted to UTF-8")
                return True
                
            except Exception as e2:
                print(f"❌ {encoding} also failed: {e2}")
        
        return False
        
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

if __name__ == "__main__":
    success = test_explorer_encoding()
    sys.exit(0 if success else 1)