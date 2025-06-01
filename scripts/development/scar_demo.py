#!/usr/bin/env python3
"""
SCAR system demonstration script
"""

def demo_scar_functionality():
    """Demonstrate SCAR system functionality"""
    try:
        from src.kimera.identity import Identity
        
        # Initialize identity system
        identity = Identity()
        
        # Demo SCAR generation
        content_a = "The sky is blue"
        content_b = "The ocean is blue"
        relationship_type = "similarity"
        
        scar_id = identity.generate_scar(content_a, content_b, relationship_type)
        print(f"Generated SCAR: {scar_id}")
        
        # Verify stability
        scar_id_2 = identity.generate_scar(content_a, content_b, relationship_type)
        
        if scar_id == scar_id_2:
            print("✅ SCAR generation is stable")
        else:
            print("❌ SCAR generation is unstable")
            
        return True
        
    except Exception as e:
        print(f"❌ SCAR demo failed: {e}")
        return False

if __name__ == "__main__":
    demo_scar_functionality()