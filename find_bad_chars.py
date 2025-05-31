#!/usr/bin/env python3
"""
Find problematic characters in explorer.html
"""

def find_bad_chars():
    """Find non-ASCII characters in the file"""
    try:
        with open("tools/explorer.html", "rb") as f:
            data = f.read()
        
        print(f"File size: {len(data)} bytes")
        
        # Find non-ASCII bytes
        bad_positions = []
        for i, byte in enumerate(data):
            if byte > 127:
                bad_positions.append((i, byte, hex(byte)))
        
        if bad_positions:
            print(f"Found {len(bad_positions)} non-ASCII bytes:")
            for pos, byte, hex_val in bad_positions[:10]:  # Show first 10
                # Get context around the bad byte
                start = max(0, pos - 10)
                end = min(len(data), pos + 10)
                context = data[start:end]
                
                # Convert context to string, replacing bad bytes
                context_str = ""
                for b in context:
                    if b > 127:
                        context_str += f"[{hex(b)}]"
                    elif 32 <= b <= 126:
                        context_str += chr(b)
                    else:
                        context_str += "."
                
                print(f"  Position {pos}: byte {hex_val} ({byte})")
                print(f"    Context: {context_str}")
                
            # Fix by removing/replacing bad bytes
            print("\nFixing file...")
            fixed_data = bytearray()
            for byte in data:
                if byte > 127:
                    # Replace with space or appropriate ASCII
                    if byte == 0x8D:  # Common smart quote issue
                        fixed_data.append(ord("'"))  # Replace with regular apostrophe
                    else:
                        fixed_data.append(ord(" "))  # Replace with space
                else:
                    fixed_data.append(byte)
            
            # Write fixed file
            with open("tools/explorer.html", "wb") as f:
                f.write(fixed_data)
            
            print("✅ Fixed file written")
            return True
        else:
            print("✅ No non-ASCII bytes found")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    find_bad_chars()