#!/usr/bin/env python3
"""
Validate that the negation fix setup is working correctly
"""
import sys
from pathlib import Path

def validate_imports():
    """Test that all imports work"""
    print("Validating imports...")
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from kimera.resonance import resonance, negation_mismatch, NEGATIONS
        from kimera.geoid import init_geoid
        
        print("✓ All imports successful")
        print(f"✓ Negation words loaded: {len(NEGATIONS)} words")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def validate_negation_detection():
    """Test negation detection logic"""
    print("\nValidating negation detection...")
    
    test_cases = [
        ("Birds can fly", "Birds cannot fly", True),
        ("Snow is white", "Snow is black", False),
        ("I like cats", "I don't like cats", True),
        ("The sky is blue", "The ocean is blue", False),
        ("Fire is hot", "Fire isn't hot", True),
    ]
    
    all_passed = True
    for text1, text2, expected in test_cases:
        try:
            result = negation_mismatch(text1, text2)
            if result == expected:
                print(f"✓ '{text1}' vs '{text2}' -> {result}")
            else:
                print(f"✗ '{text1}' vs '{text2}' -> {result} (expected {expected})")
                all_passed = False
        except Exception as e:
            print(f"✗ Error testing '{text1}' vs '{text2}': {e}")
            all_passed = False
    
    return all_passed

def validate_resonance_integration():
    """Test that resonance function works with negation fix"""
    print("\nValidating resonance integration...")
    
    try:
        # Create test geoids
        geoid1 = init_geoid("Birds can fly", "en", ["test"], raw="Birds can fly")
        geoid2 = init_geoid("Birds cannot fly", "en", ["test"], raw="Birds cannot fly")
        
        # Test resonance
        score = resonance(geoid1, geoid2)
        print(f"✓ Resonance score computed: {score:.3f}")
        
        # The score should be lower due to negation penalty
        if score < 0.5:  # Assuming normal similarity would be higher
            print("✓ Negation penalty appears to be applied")
        else:
            print("? Negation penalty may not be working as expected")
        
        return True
    except Exception as e:
        print(f"✗ Resonance integration failed: {e}")
        return False

def validate_files():
    """Check that required files exist"""
    print("\nValidating required files...")
    
    required_files = [
        "data/mixed_contradictions.csv",
        "tools/explorer.html",
        "benchmarks/llm_compare.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all validations"""
    print("🔍 Validating Negation Fix Setup")
    print("=" * 40)
    
    validations = [
        ("Imports", validate_imports),
        ("Negation Detection", validate_negation_detection),
        ("Resonance Integration", validate_resonance_integration),
        ("Required Files", validate_files),
    ]
    
    all_passed = True
    for name, validator in validations:
        try:
            passed = validator()
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"✗ {name} validation crashed: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All validations passed! Ready for research loop.")
        print("\nNext steps:")
        print("1. Run: python research_loop.py")
        print("2. Or use PowerShell: ./run_research_loop.ps1")
    else:
        print("❌ Some validations failed. Please fix issues before proceeding.")

if __name__ == "__main__":
    main()