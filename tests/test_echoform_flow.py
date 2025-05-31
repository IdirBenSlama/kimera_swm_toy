#!/usr/bin/env python3
"""
EchoForm smoke test - create → mutate → flatten → reinflate flow
"""
import sys
sys.path.insert(0, 'src')

from kimera.echoform import EchoForm


def test_echoform_basic_creation():
    """Test basic EchoForm creation and properties"""
    echo = EchoForm(anchor="Test_001")
    
    assert echo.anchor == "Test_001"
    assert echo.domain == "echo"
    assert echo.phase == "active"
    assert echo.recursive is True
    assert len(echo.terms) == 0
    assert echo.trace_signature != ""
    assert echo.echo_created_at is not None
    print("✅ Basic creation test passed")


def test_echoform_with_terms():
    """Test EchoForm creation with terms"""
    echo = EchoForm(
        anchor="Scar_007",
        terms=[
            {"symbol": "!∂Scar_007", "role": "contradiction_seed", "intensity": 1.0},
            {"symbol": "∇echo", "role": "resonance_marker", "intensity": 0.5}
        ]
    )
    
    assert len(echo.terms) == 2
    assert echo.intensity_sum() == 1.5
    assert echo.terms[0]["symbol"] == "!∂Scar_007"
    print("✅ Terms creation test passed")


def test_echoform_add_term():
    """Test adding terms to EchoForm"""
    echo = EchoForm(anchor="Test_002")
    
    echo.add_term("test_symbol", "test_role", 2.0, extra_prop="test_value")
    
    assert len(echo.terms) == 1
    assert echo.terms[0]["symbol"] == "test_symbol"
    assert echo.terms[0]["role"] == "test_role"
    assert echo.terms[0]["intensity"] == 2.0
    assert echo.terms[0]["extra_prop"] == "test_value"
    assert echo.intensity_sum() == 2.0
    print("✅ Add term test passed")


def test_echoform_phase_mutation():
    """Test phase mutation with trace chaining"""
    echo1 = EchoForm(anchor="Test_003", phase="active")
    original_trace = echo1.trace_signature
    
    echo2 = echo1.mutate_phase("dormant")
    
    assert echo1.phase == "active"  # Original unchanged
    assert echo2.phase == "dormant"  # New phase
    assert echo1.trace_signature != echo2.trace_signature  # Different traces
    assert echo2.anchor == echo1.anchor  # Same anchor
    print("✅ Phase mutation test passed")


def test_echoform_flatten_reinflate():
    """Test the core flatten → reinflate flow"""
    # Create original form
    echo1 = EchoForm(
        anchor="Scar_007",
        domain="scar",
        terms=[
            {"symbol": "!∂Scar_007", "role": "contradiction_seed", "intensity": 1.0}
        ],
        phase="active"
    )
    
    # Flatten to JSON
    blob = echo1.flatten()
    assert isinstance(blob, str)
    assert "Scar_007" in blob
    assert "contradiction_seed" in blob
    
    # Reinflate from JSON
    echo2 = EchoForm.reinflate(blob)
    
    # Verify reconstruction
    assert echo1.anchor == echo2.anchor
    assert echo1.domain == echo2.domain
    assert echo1.phase == echo2.phase
    assert echo1.trace_signature == echo2.trace_signature
    assert echo1.intensity_sum() == echo2.intensity_sum()
    assert len(echo1.terms) == len(echo2.terms)
    assert echo1.terms[0]["symbol"] == echo2.terms[0]["symbol"]
    
    print("✅ Flatten/reinflate test passed")


def test_echoform_trace_computation():
    """Test trace signature computation"""
    echo1 = EchoForm(anchor="Test_004", phase="active")
    echo2 = EchoForm(anchor="Test_004", phase="active")
    echo3 = EchoForm(anchor="Test_005", phase="active")
    
    # Same anchor + phase should give same trace
    assert echo1.trace_signature == echo2.trace_signature
    
    # Different anchor should give different trace
    assert echo1.trace_signature != echo3.trace_signature
    
    # Trace should be 16 characters
    assert len(echo1.trace_signature) == 16
    
    print("✅ Trace computation test passed")


def test_echoform_full_flow():
    """Complete smoke test: create → mutate → flatten → reinflate"""
    print("\n🔥 Running full EchoForm flow test...")
    
    # Step 1: Create
    echo1 = EchoForm(
        anchor="Scar_007",
        terms=[{"symbol": "!∂Scar_007", "role": "contradiction_seed", "intensity": 1.0}]
    )
    print(f"  Created: {echo1}")
    
    # Step 2: Mutate
    echo2 = echo1.mutate_phase("dormant")
    echo2.add_term("∇mutation", "phase_marker", 0.3)
    print(f"  Mutated: {echo2}")
    
    # Step 3: Flatten
    blob = echo2.flatten()
    print(f"  Flattened: {len(blob)} chars")
    
    # Step 4: Reinflate
    echo3 = EchoForm.reinflate(blob)
    print(f"  Reinflated: {echo3}")
    
    # Verify integrity
    assert echo2.anchor == echo3.anchor
    assert echo2.phase == echo3.phase
    assert echo2.trace_signature == echo3.trace_signature
    assert echo3.intensity_sum() == 1.3  # 1.0 + 0.3
    assert len(echo3.terms) == 2
    
    print("✅ Full flow test passed!")
    return True


def main():
    """Run all EchoForm tests"""
    print("🧪 EchoForm Core Tests")
    print("=" * 25)
    
    tests = [
        test_echoform_basic_creation,
        test_echoform_with_terms,
        test_echoform_add_term,
        test_echoform_phase_mutation,
        test_echoform_flatten_reinflate,
        test_echoform_trace_computation,
        test_echoform_full_flow
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All EchoForm tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)